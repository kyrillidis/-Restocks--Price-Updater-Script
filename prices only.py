from bs4 import BeautifulSoup
import requests
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Sheets API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r"/Users/vasiliskyrillidis/Desktop/python/og-market-price-updater-befad99fab9f.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open('panagia').sheet1

# Define the link to scrape
link = 'https://ogmarketath.com/products/nike-dunk-low-archeo-pink-w'

# Scrape the prices and sizes
response = requests.get(link)
soup = BeautifulSoup(response.content, 'lxml')
list_items = soup.find_all('li')
sizes = []
prices = []
for li in list_items:
    size = li.find('span', class_='text')
    price_1 = li.find('span', class_='price')
    price_1 = re.split('>', str(price_1))
    if size is not None:
        size = str(size)
        if price_1 is not None:
            if '€' in str(price_1):
                price_1 = re.split('<', str(price_1[2]))
                price_1 = (float(price_1[0].replace('€', '').replace('.', '')) + 45) * 1.24  # Add 45 to the price
            else:
                price_1 = None
            sizez = str(size[19:-7]).replace('½', '.5').replace(' ', '')
            sizes.append(sizez)
            prices.append(price_1)

# Write the results to the Google Sheet
size_list = [[f"{size}"] for size in sizes]
price_list = [[f"{price} €"] if price is not None else ["Not listed yet"] for price in prices]
sheet.update('Class Data!A2:A', size_list)
sheet.update('Class Data!B2:B', price_list)