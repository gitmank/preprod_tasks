# imports
import pandas as pd
import psycopg2 as pg

# connect to postgres instance
db_name = 'postgres'
db_user = 'postgres'
conn = pg.connect(dbname=db_name, user=db_user, host='127.0.0.1')
cursor = conn.cursor()

# query mock data
df = pd.read_sql_query('SELECT * FROM mock_data', conn)

# export to csv
df.to_csv('sprint_2/SQL_DATA.csv', index=False)

# commit and close
cursor.close()
conn.close()

print('🟢 Data exported successfully')