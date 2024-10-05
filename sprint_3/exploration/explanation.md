# Data Exploration DIY
> SQL queries on data from different sources using polars

### What is polars?
- Polars is essentially pandas, but with more speed and features. 
- It is a library for manipulating dataframes.

### data sources
- `MOCK_DATA.csv` - csv file of people's email, city, country and IP address
- `CAR_DATA.json` - ndjson file of a person's id and car manufacturer

##### Instructions
- run `pip install -r requirements.txt` to install dependencies
- run `python explore.py` to run the queries
  
##### Queries
- Select specific columns from the csv file
- Join csv and json data on a common column
- Filter data based on a condition
- Group data and calculate min, max, avg, sum
