import pandas as pd
import numpy as np
import json
from datetime import datetime
import time
from collections import Counter

###################### Classes ########################
class Day:
    def __init__(self, date, ucam_rec, dmp_rec):
        self.date = date
        self.ucam_rec = ucam_rec
        self.dmp_rec = dmp_rec

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

def duration_from_start_end(start, end):
    d0 = datetime.strptime(start, "%Y-%m-%d")
    d1 = datetime.strptime(end, "%Y-%m-%d")
    delta = d1 - d0
    return (delta.days)

def startWear(period):
    newP = period.split()
    d0 = datetime.strptime(period.split()[0], "%Y-%m-%d")
    return (d0)

def endWear(period):
    newP = period.split()
    d1 = datetime.strptime(period.split()[1], "%Y-%m-%d")
    return (d1)

def makeWearList():
    # create list of dates from start of project to today
    dateList = pd.date_range(start="2020-07-01",end=datetime.today()).to_pydatetime().tolist()
    # use the list to generate a list of objects each with a date and a bool depending on ucam and dmp
    wearList = []
    for date in dateList:
        wearList.append(Day(date, False, False))
    return wearList

def listFromDuration(start, duration):
    # create list of dates from start of project to today
    datelist = pd.date_range(start, periods=duration).tolist()
    return datelist

def processRecord(frame):
    print("processing the record")
    print(frame)

def formatParticipantID(id):
    id = id.replace('-', '')
    return id

def amendWearList(start, end, duration,wearList):
    # DMP data - list consecutive days of a wear period from dmp
    newList = listFromDuration(start, duration)
    # loop through newList and try and find a match within the wearList
    # matches = 0 
    for x in newList:
        for y in wearList:
            if y.date == x:
                # set dmp to true
                y.dmp_rec = True

def matching_device_check(ucam_device_id, dmp_device_id):
    result = False
    if ucam_device_id is not None:
        dmp_dev = dmp_device_id[ 0 : 3 ]
        ucam_dev = ucam_device_id[ 0 : 3 ] 
        # take the first three characters of device IDs to determin the device
        if ucam_dev == dmp_dev:
            result = True
        elif ucam_dev == 'SMP' and dmp_dev == "a device name":
            result = True
        elif ucam_dev == 'BVN' and dmp_dev == "a device name":
            result = True
        elif ucam_dev == 'PAD' and dmp_dev == "a device name":
            result = True
        elif ucam_dev == 'BTF' and dmp_dev == "a device name":
            result = True
    # else:
        # print("matching_device_check failed due to None type")
    return result


def print_report(dev_name):
    # calculate percentage of mismatches for exact days
    if mismatches_count > 0 and matches_count > 0:
        exact_mismatches_percent = float(mismatches_count) / float(matches_count) * 100
    else:
        exact_mismatches_percent = 0
    # calculate percentage of mismatches total days contributed, regardless of when these days occurred
    mismatched_total = abs(ucam_count - dmp_count) / float(ucam_count) * 100
    print("%s report: exact mismatches as percentage: %0.3f, mismatched total coverage as percentage: %0.03f, ucam says expect: %s, dmp shows we got: %s, daily matches count: %s, daily mismatches count: %s" % (dev_name, exact_mismatches_percent, mismatched_total, ucam_count, dmp_count, matches_count, mismatches_count))


def comparePeriods(df, device):
    # reset master variables
    global ucam_count
    global dmp_count
    global matches_count
    global mismatches_count
    ucam_count = 0
    dmp_count = 0
    matches_count = 0
    mismatches_count = 0
    # add usful data to the dataframe
    df['Start'] = df['Period'].apply(startWear)
    df['End'] = df['Period'].apply(endWear)
    df['Duration'] = df['Period'].apply(duration_from_period)
    # group the participants' data together
    participants = (df['Participant ID'].unique())
    print("dmp participants: %s" % (len(participants)))
    # print(participants)
    p_group = df.groupby(['Participant ID'])
    # loop through the participants' data
    for p_id in participants:
        # use a new wearlist for each participant
        wearList = makeWearList()
        # get a participants data
        p_recs = (p_group.get_group(p_id))
        # process each of their associated uploads
        for index, row in p_recs.iterrows():
            # check the start, end, duration of the DMP recs and modify wearList to reflect these dmp wear dates
            amendWearList(row['Start'], row['End'], row['Duration'],wearList)
        # loop through ucam looking for our participant
        for p in ucam['data']:
            formatted_ucam_id = formatParticipantID(p['patient_id'])
            if formatted_ucam_id == p_id:
                # we have found the UCAM entry for our current participant
                # get the data that matches our current device
                for ucam_rec in p['devices']:
                    if matching_device_check(ucam_rec['device_id'], device):
                        # do something with this matching ucam_rec...
                        # get start, end and duration;
                        start_date = ucam_rec['start_wear'].split("T")[0]
                        end_date = ucam_rec['end_wear'].split("T")[0]
                        ucam_duration = duration_from_start_end(start_date, end_date)
                        # make a new wear list - list consecutive days of a wear period from dmp
                        new_ucam_List = listFromDuration(start_date, ucam_duration)  
                        # ammend main wear list
                        for x in new_ucam_List:
                            for y in wearList:
                                if y.date == x:
                                    # set dmp to true
                                    y.ucam_rec = True 
                break
        # we should now have a wearList with dmp wear and ucam wear entries complete 
        for x in wearList:
            if x.ucam_rec == True:
                ucam_count += 1
                if x.dmp_rec == False:
                    mismatches_count += 1
            if x.dmp_rec == True:
                dmp_count += 1
                if x.ucam_rec == False:
                    mismatches_count += 1
            if x.ucam_rec == True and x.dmp_rec == True:
                 matches_count += 1
        # onto the next participant


###################### load UCAM ########################
f = open('data/ucamResponse.json',)
ucam = json.load(f)
# for key in ucam['data']: 
#         print(key)
# gather and format participant ID from UCAM
ucam_participants = []
for p in ucam['data']:
    id = p['patient_id']
    id = formatParticipantID(id)
    if id not in ucam_participants:
        ucam_participants.append(id)
print("number of ucam participants: %s" % (len(ucam_participants)))

# declare these variables
ucam_count = 0
dmp_count = 0
matches_count = 0
mismatches_count = 0

###################### Dreem  ########################
df = pd.read_csv('data/Dreem.csv')
comparePeriods(df, 'DRM')
print_report('Dreem')

###################### ThinkFast ########################
# NOT WORKING
# df = pd.read_csv('data/tfa_data.csv')
# comparePeriods(df, 'TFA')
# print_report('ThinkFast')

###################### VTT eBedSensor ########################
df = pd.read_csv('data/VTTBedSensor.csv')
comparePeriods(df, 'BED')
print_report('VTT eBedSensor')


###################### VTT SMA ########################
df = pd.read_csv('data/StressMonitorApp.csv')
comparePeriods(df, 'SMA')
print_report('VTT SMA')

###################### Vital Patch ########################
df = pd.read_csv('data/VitalPatch.csv')
comparePeriods(df, 'VTP')
print_report('Vital Patch')

###################### Axivity ########################
df = pd.read_csv('data/Axivity.csv')
comparePeriods(df, 'AX6')
print_report('Axivity')

###################### McRoberts ########################
df = pd.read_csv('data/StressMonitorApp.csv')
comparePeriods(df, 'MMM')
print_report('McRobertsn Move Monitor')

###################### ZKOne ########################
df = pd.read_csv('data/ZKOne.csv')
comparePeriods(df, 'YSM')
print_report('ZKOne')

###################### Everion ########################


###################### Byteflies ########################

