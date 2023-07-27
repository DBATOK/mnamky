import requests
from bs4 import BeautifulSoup
import pandas as pd

class WebsiteScraper:
    def __init__(self, start_url):
        # Initialize an empty list to store the data
        self.data = []
        self.url = start_url

    def scrape_website(self):
        while self.url:
            # Get the HTML content of the current page
            response = requests.get(self.url)
            # Parse HTML code for the entire site
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Find mnamky blocks
            mnamky = soup.find_all('div', class_='entry entry-block entry-articles')
            
            # Loop through mnamky to find attributes
            for mnamka in mnamky:
                self.extract_data(mnamka)
            
            self.find_next_page(soup)

    def extract_data(self, mnamka):
        # Find attributes
        title = mnamka.find('h3', class_='entry-title').find('a').text
        summary = mnamka.find('p', class_='entry-body__text').text
        # Remove line breaks from summary
        summary = summary.replace('\n', '')
        url_att = mnamka.find('h3', class_='entry-title').find('a')['href']
        img_url = self.extract_image_url(mnamka, title)
        # Append to the list of dictionaries
        self.data.append({'title': title, 'summary': summary, 'url': url_att, 'img_url': img_url})

    def extract_image_url(self, mnamka, title):
        try:
            img_url = mnamka.find('div', class_='entry-media entry-media-left').find('img')['data-srcset'].split(' ')[0]
        except:
            try:
                img_url = mnamka.find('img')['src']
                #print(title)
                #print('success')
            except:
                img_url = ''
                #print(title)
                #print('fail')
        return img_url

    def find_next_page(self, soup):
        next_button = soup.find('li', class_='pagination-next')
        # Check if the next button exists
        if next_button.find('a'):
            self.url = next_button.find('a')['href']
            print(self.url)
            # Concatenate the base url with the relative url
            self.url = 'https://www.bizztreat.com' + self.url
        else:
            self.url = None

# Instantiate the scraper object
scraper = WebsiteScraper("https://www.bizztreat.com/bizztro")

# Use the scraper object to scrape the website
scraper.scrape_website()

# Convert the list of dictionaries into a DataFrame
df = pd.DataFrame(scraper.data)

# Save the DataFrame to a CSV file
df.to_csv('mnamky.csv', index=False, sep='~')