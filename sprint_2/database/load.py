# imports 
import os
import pandas as pd
import threading
from pymongo import MongoClient # python library for mongodb connections

# config
MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017') # database connection string
FILE_PATH = 'sprint_2/MOCK_DATA.csv'

def csv_to_mongo():
    try:
        # connect to mongodb
        client = MongoClient(MONGO_URI)
        db = client['preprod-db']
        mock_data = db['mock-data']

        # load data to pandas dataframe
        df = pd.read_csv(FILE_PATH)
        print(df.head())

        # insert row as document
        def insert_row(row):
            data = row[1].to_dict()
            mock_data.insert_one(data)

        # we're using threads so we don't have to wait for each row to be inserted
        threads = []
        for row in df.iterrows():
            thread = threading.Thread(target=insert_row, args=(row,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()

        print('🟢 Data exported successfully')
    except Exception as e:
        print('🔴 Error exporting from mongo')
        print(str(e))

if __name__ == '__main__':
    csv_to_mongo()