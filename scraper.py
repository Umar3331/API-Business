import sqlite3
import requests
from bs4 import BeautifulSoup

# Scrape eBay for products
def scrape_ebay():
    url = "https://www.ebay.co.uk/sch/i.html?_nkw=watches"
    response = requests.get(url)
    print(f"Status Code: {response.status_code}")
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup.prettify())  # This should print the entire HTML page
    items = soup.find_all('li', class_='vl-carousel__item')
    print(f"Found {len(items)} items.")

    data = []
    if not items:
        print("No items found on the page. Please check the CSS selectors.")
        return data

    for item in items:
        try:
            # Extract the product link
            product_link = item.find('a', class_='vlp-merch-item-tile')['href']

            # Extract the product title
            title = item.find('h3', class_='vlp-merch-item-title').text

            # Extract the product price
            price = item.find('span', role='text').text

            # Extract the product image URL
            img_url = item.find('img', class_='vlp-merch-item-image')['src']

            print(f"Scraped title: {title}, Price: {price}, Image: {img_url}, Link: {product_link}")
            data.append((title, price, img_url, product_link))

        except Exception as e:
            print(f"Error scraping item: {e}")

    return data

# Store scraped data in SQLite
def store_data(data):
    if not data:
        print("No data to store. Exiting.")
        return
    conn = sqlite3.connect('/data/ebay_data.db')  # Use the correct mounted volume path
    c = conn.cursor()

    # Drop the existing products table if it exists
    c.execute('''DROP TABLE IF EXISTS products''')

    # Create the table with the new schema
    c.execute('''CREATE TABLE products (title TEXT, price TEXT, img_url TEXT, link TEXT)''')

    # Insert the scraped data
    c.executemany('INSERT INTO products (title, price, img_url, link) VALUES (?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    data = scrape_ebay()
    store_data(data)
    print(f"Scraped {len(data)} items from eBay")
