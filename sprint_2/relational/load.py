# imports
import pandas as pd
import psycopg2 as pg

# load csv file as pandas dataframe
df = pd.read_csv('sprint_2/MOCK_DATA.csv')
print(df.head())

# connect to postgres instance
db_name = 'postgres'
db_user = 'postgres'
conn = pg.connect(dbname=db_name, user=db_user, host='127.0.0.1')
cursor = conn.cursor()

# create table
cursor.execute('CREATE TABLE IF NOT EXISTS mock_data (id SERIAL, email VARCHAR(255), gender VARCHAR(255), ip VARCHAR(255), city VARCHAR(255), country VARCHAR(255), size VARCHAR(255), weight VARCHAR(255))')

# query template
query = 'INSERT INTO mock_data (id, email, gender, ip, city, country, size, weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'

# iterate over dataframe rows
for row in df.iterrows():
    cursor.execute(query, tuple(row[1]))

# commit and close
conn.commit()
cursor.close()
conn.close()

print('🟢 Data loaded successfully')