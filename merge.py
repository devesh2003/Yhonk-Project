import glob
import pandas as pd
import os

def merge():

    if os.path.isfile('data.csv'):
        os.remove('data.csv')

    files = glob.glob("*.csv")
    columns = ['Bus Body','Date','Packet','Slot','Latitude','Longitude','Place']
    df = []
    for file in files:
        data = pd.read_csv(file)
        data.columns = columns
        os.remove(file)
        df.append(data)
    newdf = pd.concat(df)
    newdf.to_csv('data.csv',index=False)