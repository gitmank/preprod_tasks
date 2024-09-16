# imports 
import os
import pandas as pd
from pymongo import MongoClient # python library for mongodb connections

# config
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017') # database connection string
EXPORT_PATH = 'sprint_2/MONGO_DATA.csv'

def mongo_to_csv():
    try:
        # connect to mongodb
        client = MongoClient(MONGO_URI)
        db = client['preprod-db']
        mock_data = db['mock-data']
        all_records = mock_data.find().sort('id', 1)

        # convert to dataframe
        df = pd.DataFrame(list(all_records))

        # write to csv
        df.drop(columns=['_id'], inplace=True)
        df.to_csv(EXPORT_PATH, index=False, header=True)
        print(df.head())

        print('🟢 Data imported successfully')
    except Exception as e:
        print('🔴 Error exporting from mongo')
        print(str(e))

if __name__ == '__main__':
    mongo_to_csv()