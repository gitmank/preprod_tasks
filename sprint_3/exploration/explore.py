import polars as pl

# import data from csv
people = pl.read_csv("../MOCK_DATA.csv")
print(people.head())
print("✅ Import data from csv\n")

# import data from json
cars = pl.read_ndjson("../CAR_DATA.json")
print(cars.head())
print("✅ Import data from json\n")

# exectute simple select query
with pl.SQLContext(register_globals=True, eager=True) as ctx:
    geo_details = ctx.execute("SELECT id, ip_address, city, country FROM people")
    print(geo_details.head())
    print("✅ Select some columns\n")

# execute join query on two dataframes
with pl.SQLContext(register_globals=True, eager=True) as ctx:
    car_and_city = ctx.execute("SELECT people.id, people.email, cars.car, people.city, people.country FROM people INNER JOIN cars ON people.id = cars.id WHERE cars.car = 'Honda'")
    print(car_and_city.head())
    print("✅ Find people in MOCK_DATA who own a Honda in CAR_DATA\n")

# execute aggregate queries
with pl.SQLContext(register_globals=True, eager=True) as ctx:
    weight_by_country = ctx.execute("SELECT country, SUM(weight) as total_weight, AVG(weight) as avg_weight, MAX(weight) as max_weight, MIN(weight) as min_weight FROM people GROUP BY country ORDER BY max_weight - avg_weight DESC")
    print(weight_by_country.head())
    print("✅ Find sum, avg, max, min of weight of people by country\n")