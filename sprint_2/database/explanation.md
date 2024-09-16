# Data Sources
> using data from ftp, web scraping and databases for data science

### MongoDB as a data source
+ document dbs are flexible and don't have a strict schema
- they don't support complex queries

##### Test MongoDB container
> using docker
run `docker run -p 27017:27017 -d mongo` to start MongoDB
use default connection string `mongodb://localhost:27017/` to connect to the database

##### load csv to MongoDB
> using pandas and pymongo
run `load.py` to insert rows from `MOCK_DATA.csv` to the database

##### exporting data from MongoDB
> using pandas and pymongo
run `dump.py` to load documents from database as a pandas dataframe and save it as a csv file
