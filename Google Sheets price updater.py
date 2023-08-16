from bs4 import BeautifulSoup
import requests
import re
import os
import os.path
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from time import sleep, time

start_time = time()  # Start timing

# Authenticate with Google Sheets API
scope = ['https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name(r"/Users/.../Desktop/python/og-market-price-updater-befad99fab9f.json", scope)
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open('price updater').sheet1

#Read the links from the text file
#with open(r"/Users/.../Desktop/New folder/links.txt") as f:
#    links = f.readlines()
    
#Define the links to scrape
links = ['https://restocks.net/en/p/air-jordan-4-retro-red-thunder',
         'https://restocks.net/en/p/nike-sb-x-air-jordan-4-retro-pine-green',
         'https://restocks.net/en/p/air-jordan-4-se-craft-photon-dust',
         'https://restocks.net/en/p/air-jordan-4-retro-white-midnight-navy',
         'https://restocks.net/en/p/air-jordan-4-retro-se-black-canvas',
         'https://restocks.net/en/p/air-jordan-4-retro-military-black',
         'https://restocks.net/en/p/air-jordan-4-retro-oil-green-w',
         'https://restocks.net/en/p/air-jordan-4-retro-canyon-purple-w',
         'https://restocks.net/en/p/air-jordan-1-retro-low-og-sp-x-travis-scott-olive-w',
         'https://restocks.net/en/p/adidas-yeezy-boost-350-v2-bone',
         'https://restocks.net/en/p/yeezy-boost-350-v2-197221',
         'https://restocks.net/en/p/adidas-yeezy-boost-350-v2-dazzling-blue',
         'https://restocks.net/en/p/adidas-yeezy-boost-350-v2-mx-oat',
         'https://restocks.net/en/p/adidas-yeezy-boost-350-v2-onyx',
         'https://restocks.net/en/p/adidas-yeezy-boost-350-v2-beluga-reflective',
         'https://restocks.net/en/p/yeezy-boost-350-v2-f99710-sesame',
         'https://restocks.net/en/p/adidas-yeezy-boost-350-v2-slate-core-black-slate',
         'https://restocks.net/en/p/adidas-yeezy-boost-350-v2-clay-us-region-release-91922']

# Loop through each link and scrape the prices and sizes
for i in range(len(links)):
    s, p, size_list = [], [], []
    response = requests.get(links[i])
    soup = BeautifulSoup(response.content, 'lxml')
    name = soup.find('meta', {'property': 'og:title'})['content']
    name = re.split('-', str(name))
    name = name[0]
    sku = soup.find('meta', {'property': 'og:image'})['content']
    sku = re.split('/', str(sku))
    position = len(sku)
    sku = sku[position - 2]
    name = str(name)

    list_items = soup.find_all('li')
    for li in list_items:
        size = li.find('span', class_='text')
        price_1 = li.find('span', class_='price')
        price_1 = re.split('>', str(price_1))
        if size is not None:
            size = str(size)
            if price_1 is not None:
                if '€' in str(price_1):
                    price_1 = re.split('<', str(price_1[2]))
                    price_1 = str(price_1[0]).replace('€', '').replace('.', '') # remove all dots
                    sizez = str(size[19:-7]).replace('½', '.5')
                    sizez = str(sizez).replace(' ', '')
                    if sizez not in s:
                        s.append(sizez)
                        p.append((float(price_1) + 55) * 1.25)
                else:
                    sizez = str(size[19:-7]).replace('½', '.5')
                    sizez = str(sizez).replace(' ', '')
                    if sizez not in s:
                        s.append(sizez)
                        p.append(None)


    # Write the results to the Google Sheet
    size_list = [f"{s[idx]} - [{p[idx]} €]" if p[idx] is not None else f"{s[idx]} - [Not listed yet]"
                 for idx in range(len(s))]
    sheet.insert_row([name, sku] + size_list, index=2)

end_time = time()  # End timing
runtime = end_time - start_time  # Calculate runtime in seconds

print("Runtime: {:.2f} seconds".format(runtime))  # Print runtime