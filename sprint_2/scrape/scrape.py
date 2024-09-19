# import beatifulsoup for scraping
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

# request html page
url = 'https://webscraper.io/test-sites/e-commerce/allinone' # free test site
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html_page = urlopen(req).read()

# scrape the page with bs4
soup = BeautifulSoup(html_page, 'lxml')

# find product details
products = soup.find_all('div', class_='product-wrapper')
product_names = []
product_prices = []
product_descriptions = []
product_reviews = []
# loop through products and print product name
for product in products:
    product_names.append(product.find('a', class_='title')['title'])
    product_prices.append(product.find('h4', class_='price').text)
    product_descriptions.append(product.find('p', class_='description').text)
    product_reviews.append(product.find('p', class_='review-count').text.split(' ')[0])

# create pandas dataset
df = pd.DataFrame({'Name': product_names, 'Price': product_prices, 'Description': product_descriptions, 'Reviews': product_reviews})
print(df.head())

# save to csv
df.to_csv('sprint_2/SCRAPED_DATA.csv', index=False, encoding='utf-8')


