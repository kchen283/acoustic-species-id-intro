from datetime import datetime
from dateutil import parser
import pandas as pd
import re

from pathlib import Path  
filepath = Path('out.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  

def convert_time (string):
    time = datetime.strptime(string, '%H:%M:%S')
    return time.hour


def random_sample (path):
    #read CSV File
    data = pd.read_csv(path, usecols= {0,11,12,14}, parse_dates=['StartDateTime'])    
    df = pd.read_csv(path) #holds original values unchanged

    #use values with duration greater than 60 seconds
    data = data[data['Duration'] > 60.0]
    listSample = [] #list to store the random samples

    #creates time and cuts down to just hour (0 - 24)
    data = data.dropna(subset=['Comment'])
    data['Comment'] = data['Comment'].str.split().str[2]
    data['Comment'] = data['Comment'].apply(convert_time)

    #loop to generate a list for each hour, then select random data
    '''
    AM-18 only had a select number of hours, so couldn't get 24 clips
    AM-19 No files
    AM-21 No files
    AM-28 No Files
    '''
    num_wwf = 1
    for i in range (0,36):        #loop for each AudioMoth file
        num = (str) (i) 
        if (i <= 30):
            audioMothList = data[data['AudioMothCode']=='AM-'+num]
        else:
            audioMothList = data[data['AudioMothCode']=='WWF-'+str(num_wwf)]
            num_wwf+=1

        if (audioMothList.empty == False):   #checks if AM is empty
            for x in range (0,24):     #loop for each hour of the day
                hourList = audioMothList[audioMothList['Comment'] == x]
                if hourList.empty:     #checks if hour is empty
                    continue
                else:
                    hourSample = hourList.sample().index.values.astype(int)
                    listSample.extend(hourSample)


    data = df.loc[listSample]
    
    return data.to_csv(filepath)