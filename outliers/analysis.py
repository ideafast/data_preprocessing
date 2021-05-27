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


###################### Dreem ########################

df = pd.read_csv('data/db_export_24_05_20.csv')

DRM = df.loc[df['device_type'] == "DRM"]
dreem = {'count': 0, 'outsideIQR': 0, 'percentOutsideIQR': 0, 'manualBoundErrorCount': 0, 'manualBoundErrorsAsPercentage': 0, 'mean': 0, 'std': 0, 'twoSDOutliersPercent': 0}
dreem['count'] = DRM.count()[0]
dreem['mean'] = pd.to_numeric(DRM['meta.filesize'], errors='coerce').fillna(0).mean() 
dreem['std'] = pd.to_numeric(DRM['meta.filesize'], errors='coerce').fillna(0).std() 
dreem_fileS = pd.to_numeric(DRM['meta.filesize'], errors='coerce').fillna(0)
Q1 = dreem_fileS.quantile(0.25)
Q3 = dreem_fileS.quantile(0.75)
IQR = Q3 - Q1
dreem['outsideIQR'] = ((dreem_fileS < (Q1 - 1.5 * IQR)) | (dreem_fileS > (Q3 + 1.5 * IQR))).sum()
dreem['percentOutsideIQR'] = np.float64(dreem['outsideIQR']) / np.float64(dreem['count']) * 100
sizes = pd.to_numeric(DRM['meta.filesize'], errors='coerce').fillna(0)
dreem['manualBoundErrorCount'] = (sizes < 100000000.0).values.sum()
dreem['manualBoundErrorsAsPercentage'] = np.float64(dreem['manualBoundErrorCount']) / np.float64(dreem['count']) * 100
d_ll = dreem['mean'] - 2 * dreem['std']
d_ul = dreem['mean'] + 1.5 * dreem['std']
d_outliers = (dreem_fileS > d_ul)
dreem['twoSDOutliersPercent'] = np.float64(d_outliers.values.sum()) / np.float64(dreem['count']) * 100

print("DreemOrig: mean file size: %.0f MB" % (dreem['mean'] / 1000000))
print("DreemOrig: standard deviation: %.0f MB" % (dreem['std'] / 1000000))
print("DreemOrig: percentage of outliers (outside the IQR*1.5): %.0f" % dreem['percentOutsideIQR'])
print("DreemOrig: percentage of outliers (manual threshold): %.0f" % dreem['manualBoundErrorsAsPercentage'])
print("DreemOrig: percentage of outliers (2 standard deviations): %.0f" % dreem['twoSDOutliersPercent'])

###################### Dreem from UCAM ########################
df = pd.read_csv('data/Dreem.csv')
stats_for_dmp_sources(df, 'Dreem - ucam')

###################### ThinkFast ########################

# df = pd.read_csv('tfa_data.csv')
# TFA = df.loc[df['device_type'] == "TFA"]
# print(TFA.columns)
# thinkF = {'count': 0, 'outsideIQR': 0, 'percentOutsideIQR': 0, 'manualBoundErrorCount': 0, 'manualBoundErrorsAsPercentage': 0, 'mean': 0, 'std': 0, 'twoSDOutliersPercent': 0}
# thinkF['count'] = TFA.count()[0]
# thinkF['mean'] = pd.to_numeric(TFA['meta.filesize'], errors='coerce').fillna(0).mean() 
# thinkF['std'] = pd.to_numeric(TFA['meta.filesize'], errors='coerce').fillna(0).std() 
# thinkF_fileS = pd.to_numeric(TFA['meta.filesize'], errors='coerce').fillna(0)
# Q1 = thinkF_fileS.quantile(0.25)
# Q3 = thinkF_fileS.quantile(0.75)
# IQR = Q3 - Q1
# thinkF['outsideIQR'] = ((thinkF_fileS < (Q1 - 1.5 * IQR)) | (thinkF_fileS > (Q3 + 1.5 * IQR))).sum()
# thinkF['percentOutsideIQR'] = np.float64(thinkF['outsideIQR']) / np.float64(thinkF['count']) * 100
# sizes = pd.to_numeric(TFA['meta.filesize'], errors='coerce').fillna(0)
# thinkF['manualBoundErrorsAsPercentage'] = np.float64(thinkF['manualBoundErrorCount']) / np.float64(thinkF['count']) * 100
# t_ll = thinkF['mean'] - 2 * thinkF['std']
# t_ul = thinkF['mean'] + 1.5 * thinkF['std']
# t_outliers = (thinkF_fileS > t_ul)
# thinkF['twoSDOutliersPercent'] = np.float64(d_outliers.values.sum()) / np.float64(thinkF['count']) * 100

# print("thinkF: mean file size: %.0f bytes" % thinkF['mean'])
# print("thinkF: standard deviation: %.0f bytes" % thinkF['std'])
# print("thinkF: percentage of outliers (outside the IQR*1.5): %.0f" % thinkF['percentOutsideIQR'])
# print("thinkF: percentage of outliers (2 standard deviations): %.0f" % thinkF['twoSDOutliersPercent'])

###################### VTT eBedSensor ########################
df = pd.read_csv('data/VTTBedSensor.csv')
stats_for_dmp_sources(df, 'VTTBedSensor')


###################### VTT SMA ########################
df = pd.read_csv('data/StressMonitorApp.csv')
stats_for_dmp_sources(df, 'VTT SMA')

###################### Vital Patch ########################
df = pd.read_csv('data/VitalPatch.csv')
stats_for_dmp_sources(df, 'Vital Patch')

###################### Axivity ########################
df = pd.read_csv('data/Axivity.csv')
stats_for_dmp_sources(df, 'Axivity')

###################### McRoberts ########################
df = pd.read_csv('data/StressMonitorApp.csv')
stats_for_dmp_sources(df, 'McRoberts')

###################### ZKOne ########################
df = pd.read_csv('data/ZKOne.csv')
stats_for_dmp_sources(df, 'ZKOne')

###################### Everion ########################


###################### Byteflies ########################

