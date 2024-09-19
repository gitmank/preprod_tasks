# Data Sources
> using data from ftp, web scraping and databases for data science

### PostgreSQL as a data source
- relational dbs have a strict schema
+ they support complex queries

##### Test PostgreSQL container
> using docker
run `docker run -p 5432:5432 -d -e POSTGRES_HOST_AUTH_METHOD=trust postgres` to init db

##### load csv to PostgreSQL
> using pandas and pymongo
run `load.py` to insert rows from `MOCK_DATA.csv` to the database

##### exporting data from PostgreSQL
> using pandas and pymongo
run `dump.py` to export data from database to a csv file
