import threading
import sqlite3
import requests
from bs4 import BeautifulSoup
import time

MAX_RETRIES = 3

class ScrapingStateManager:
    def __init__(self):
        self.lock = threading.Lock()  # Lock for thread-safe operations
        self.failed_requests = []  # Store failed requests to retry later

    def add_failed_request(self, request_info):
        with self.lock:
            self.failed_requests.append(request_info)

    def get_and_clear_failed_requests(self):
        with self.lock:
            requests = self.failed_requests.copy()
            self.failed_requests.clear()
        return requests

class HotelScraper:
    def __init__(self, db_name):
        self.db_name = db_name
        self.state_manager = ScrapingStateManager()

    def create_database(self):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS hotels (id INTEGER PRIMARY KEY, name TEXT, price TEXT)''')
        con.commit()
        con.close()

    def save_hotel_info(self, hotel_info):
        con = sqlite3.connect(self.db_name)
        cur = con.cursor()
        cur.execute('INSERT INTO hotels (name, price) VALUES (?, ?)', (hotel_info['name'], hotel_info['price']))
        con.commit()
        con.close()

    def scrape_hotel(self, url):
        for attempt in range(MAX_RETRIES):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raise an error for bad responses
                soup = BeautifulSoup(response.text, 'html.parser')
                hotel_info = self.parse_hotel(soup)
                self.save_hotel_info(hotel_info)
                return
            except requests.exceptions.RequestException as e:
                print(f'Error scraping {url}: {e}')
                self.state_manager.add_failed_request(url)
                time.sleep(2)  # Wait before retrying
                if attempt < MAX_RETRIES - 1:
                    continue  # Retry if attempt is less than max retries
                else:
                    print(f'Max retries reached for {url}.')
            finally:
                print(f'Cleanup resources for {url}')  # Placeholder for resource cleanup

    def parse_hotel(self, soup):
        # Placeholder for parsing logic
        # Example: Extract hotel name and price
        name = soup.find('h1', class_='hotel-name').get_text(strip=True)
        price = soup.find('span', class_='hotel-price').get_text(strip=True)
        return {'name': name, 'price': price}

    def run(self, urls):
        self.create_database()
        threads = []
        for url in urls:
            thread = threading.Thread(target=self.scrape_hotel, args=(url,))
            threads.append(thread)
            thread.start()
        for thread in threads:
            thread.join()  # Wait for all threads to complete

if __name__ == '__main__':
    db_name = 'hotels.db'
    urls = ['http://example.com/hotel1', 'http://example.com/hotel2']  # Replace with actual URLs
    scraper = HotelScraper(db_name)
    scraper.run(urls)
