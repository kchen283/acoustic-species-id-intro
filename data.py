import datetime
import pandas as pd

from pathlib import Path  
filepath = Path('folder/out.csv')  
filepath.parent.mkdir(parents=True, exist_ok=True)  



def random_sample (path):
    #read CSV File
    data = pd.read_csv(path, usecols= {0,11,12}, parse_dates=['StartDateTime'])       
    df = pd.read_csv(path) #holds original values unchanged

    #drop NA values
    data = data.dropna()

    #use values with duration greater than 60 seconds
    data = data[data['Duration'] > 60.0]
    listSample = [] #list to store the random samples

    #creates time and cuts down to just hour (0 - 24)
    time = pd.Series(data.StartDateTime).dt.hour
    data.insert(loc=2, column='Hour', value=time)

    #loop to generate a list for each hour, then select random data
    '''
    AM-18 only had a select number of hours, so couldn't get 24 clips
    AM-19 No files
    AM-21 No files
    AM-28 No Files
    '''
    for i in range (0,31):        #loop for each AudioMoth file
        num = (str) (i) 
        audioMothList = data[data['AudioMothCode']=='AM-'+num]
        if audioMothList.empty:   #checks if AM is empty
                continue
        else:
            for x in range (0,24):     #loop for each hour of the day
                hourList = audioMothList[audioMothList['Hour'] == x]
                if hourList.empty:     #checks if hour is empty
                    continue
                else:
                    hourSample = hourList.sample().index.values.astype(int)
                    listSample.extend(hourSample)


    data = df.loc[listSample]
    
    return data.to_csv(filepath)