from bs4 import BeautifulSoup
import requests
import time

# URL of the eBay search page
URL = "https://www.ebay.co.uk/sch/i.html?_nkw=watches"

# Function to scrape eBay
def scrape_ebay():
    response = requests.get(URL)
    soup = BeautifulSoup(response.text, 'html.parser')
    time.sleep(5)  # Adjusted waiting time for page to load

    items = soup.find_all('div', class_='s-item')
    print(f"Found {len(items)} items.")

    if not items:
        print("No items found on the page. Please check the CSS selectors.")
        return

    scraped_data = []
    
    for item in items:
        try:
            title_element = item.find('h3', class_='s-item__title')
            price_element = item.find('span', class_='s-item__price')
            link_element = item.find('a', class_='s-item__link')
            image_element = item.find('img', class_='s-item__image-img')

            title = title_element.text if title_element else "No title available"
            price = price_element.text if price_element else "No price available"
            link = link_element['href'] if link_element else "No link available"
            image = image_element['src'] if image_element else "No image available"

            print(f"Scraped title: {title}, Price: {price}, Image: {image}, Link: {link}")

            scraped_data.append({
                'title': title,
                'price': price,
                'image': image,
                'link': link
            })

        except AttributeError as e:
            print(f"Error scraping item: {e}")
    
    if scraped_data:
        print("Successfully scraped data:")
        print(scraped_data)
    else:
        print("No data scraped.")

if __name__ == "__main__":
    scrape_ebay()
