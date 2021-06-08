import pandas as pd
import numpy as np
import json
from datetime import datetime
import time

###################### Functions ########################
def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if ' B' in x:
        if len(x) > 1:
            return float(x.replace(' B', ''))
        return 1.0
    if ' KB' in x:
        if len(x) > 1:
            return float(x.replace(' KB', '')) * 1000
        return 1000.0
    if ' MB' in x:
        if len(x) > 1:
            return float(x.replace(' MB', '')) * 1000000
        return 1000000.0
    if ' GB' in x:
        return float(x.replace(' GB', '')) * 1000000000
    return 0.0

def duration_from_period(period):
    newP = period.split()
    d0 = datetime.strptime(period.split()[0], "%Y-%m-%d")
    d1 = datetime.strptime(period.split()[1], "%Y-%m-%d")
    delta = d1 - d0
    return (delta.days)

def meanOfList(num):
    sumOfNumbers = 0
    for t in num:
        sumOfNumbers = sumOfNumbers + t
    mean = sumOfNumbers / len(num)
    return mean

def stats_for_dmp_sources(df, device, lower_bound=1):
    df['Size'] = df['Size'].apply(value_to_float)
    df['duration'] = df['Period'].apply(duration_from_period)
    df['sizePerDay'] = df['Size'] / df['duration']

    stats = {'count': 0, 'outsideIQR': 0, 'percentOutsideIQR': 0, 'manualBoundErrorCount': 0, 'manualBoundErrorsAsPercentage': 0, 'mean': 0, 'std': 0, 'twoSDOutliersPercent': 0}
    stats['count'] = df.count()[0]
    stats['mean'] = df['Size'].mean() 
    stats['std'] = df['Size'].std() 
    Q1 = df['Size'].quantile(0.25)
    Q3 = df['Size'].quantile(0.75)
    IQR = Q3 - Q1
    stats['outsideIQR'] = ((df['Size'] < (Q1 - 1.5 * IQR)) | (df['Size'] > (Q3 + 1.5 * IQR))).sum()
    stats['percentOutsideIQR'] = np.float64(stats['outsideIQR']) / np.float64(stats['count']) * 100
    # stats['manualBoundErrorCount'] = (df['Size'] < lower_bound).values.sum()
    # stats['manualBoundErrorsAsPercentage'] = np.float64(stats['manualBoundErrorCount']) / np.float64(stats['count']) * 100
    ll = stats['mean'] - 2 * stats['std']
    ul = stats['mean'] + 2 * stats['std']
    outliers = ((df['Size'] > ul) | (df['Size'] < ll))
    stats['twoSDOutliersPercent'] = np.float64(outliers.values.sum()) / np.float64(stats['count']) * 100

    print("%s: mean file size: %.0f MB" % (device, stats['mean'] / 1000000))
    print("%s: standard deviation: %.0f MB" % (device, stats['std'] / 1000000))
    print("%s: percentage of outliers (outside the IQR*1.5): %.0f" % (device, stats['percentOutsideIQR']))
    # print("%s: percentage of outliers (manual threshold): %.0f" % (device, stats['manualBoundErrorsAsPercentage']))
    print("%s: percentage of outliers (2 standard deviations): %.0f" % (device, stats['twoSDOutliersPercent']))

def perPatientVariance(df, device):
    df['Size'] = df['Size'].apply(value_to_float)
    df['duration'] = df['Period'].apply(duration_from_period)
    df['sizePerDay'] = df['Size'] / df['duration']

    stats = {'count': 0, 'perPatientPerDayV': 0, 'mean': 0, 'std': 0}
    stats['count'] = df.count()[0]
    stats['mean'] = df['sizePerDay'].mean() 
    stats['std'] = df['sizePerDay'].std() 
    normalizedStandardDeviation = []

    participants = (df['Participant ID'].unique())
    for p_id in participants:
        p_recs = df.loc[df['Participant ID'] == p_id]
        # normalised standard deviation (std/mean)
        normStd = p_recs['sizePerDay'].std() / p_recs['sizePerDay'].mean()
        normalizedStandardDeviation.append(normStd)
        # print("%s for participant %s: normalised standard deviation of file size: %.0f percent" % (device, p_id, normStd))

    avDev = np.nanmean(normalizedStandardDeviation)
    print("average file size deviation for patients using %s: %.2f" % (device, avDev))
    

###################### Dreem ########################

# df = pd.read_csv('data/db_export_24_05_20.csv')

# DRM = df.loc[df['device_type'] == "DRM"]
# dreem = {'count': 0, 'mean': 0, 'std': 0}
# dreem['count'] = DRM.count()[0]
# dreem['mean'] = pd.to_numeric(DRM['meta.filesize'], errors='coerce').fillna(0).mean() 
# dreem['std'] = pd.to_numeric(DRM['meta.filesize'], errors='coerce').fillna(0).std() 

# print("DreemOrig: mean file size: %.0f MB" % (dreem['mean'] / 1000000))
# print("DreemOrig: standard deviation: %.0f MB" % (dreem['std'] / 1000000))

###################### Dreem from UCAM ########################
df = pd.read_csv('data/Dreem.csv')
perPatientVariance(df, 'Dreem - ucam')

###################### VTT eBedSensor ########################
df = pd.read_csv('data/VTTBedSensor.csv')
perPatientVariance(df, 'VTTBedSensor')


###################### VTT SMA ########################
df = pd.read_csv('data/StressMonitorApp.csv')
perPatientVariance(df, 'VTT SMA')

###################### Vital Patch ########################
df = pd.read_csv('data/VitalPatch.csv')
perPatientVariance(df, 'Vital Patch')

###################### Axivity ########################
df = pd.read_csv('data/Axivity.csv')
perPatientVariance(df, 'Axivity')

###################### McRoberts ########################
df = pd.read_csv('data/StressMonitorApp.csv')
perPatientVariance(df, 'McRoberts')

###################### ZKOne ########################
df = pd.read_csv('data/ZKOne.csv')
perPatientVariance(df, 'ZKOne')

###################### ThinkFast ########################
# No deviation of thinkfast data

###################### Everion ########################
# No data available at this time

###################### Byteflies ########################
# Complicated by the multiple sensors used in the device
