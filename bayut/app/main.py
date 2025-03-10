import requests
import time
from bs4 import BeautifulSoup
import sqlite3

# Function to scrape a single page and insert data into the database
def scrape_page(url, conn):


    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)

    print("url " + url)
    soup = BeautifulSoup(response.text, 'html.parser')


    time.sleep(1)

    # Extract data from the webpage using BeautifulSoup
    # Modify this part according to the structure of the web page you're scraping

    # Example: Extracting property details like title and price
    property_listings = soup.find_all('li', class_='a37d52f0')

    for listing in property_listings:
        # print(listing)
        title = listing.find('h2', class_='f0f13906').text.strip()
        price = listing.find('span', class_='dc381b54').text.strip()
        location = listing.find('h3', class_='_4402bd70').text.strip()
        sqft = listing.find('h4', class_="cfac7e1b _85ddb82f").text.strip()
        link_div = listing.find('a', class_='d40f2294')
        link = link_div['href']




        # Insert data into the SQLite database
        cursor = conn.cursor()
        cursor.execute("INSERT INTO properties (title, price, location,sqft,link) VALUES (?, ?, ?, ?,?)", (title, price, location, sqft, link))
        conn.commit()

# Create SQLite database and table
conn = sqlite3.connect('property_data.db')
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS properties (title TEXT, price TEXT, location TEXT, sqft TEXT, link TEXT)")

# Scrape all pages
base_url = "https://www.bayut.com/for-sale/studio-apartments/dubai/"

# this line for testing on single page
# scrape_page(url, conn)

total_pages = 3  # Modify this value based on the total number of pages to scrape

for page in range(1, total_pages + 1):
    url = base_url + "jumeirah-village-circle-jvc/page-" + str(page)  + "/?sort=price_asc&price_max=500000&completion_status=ready"
    scrape_page(url, conn)

# Close the database connection
conn.close()