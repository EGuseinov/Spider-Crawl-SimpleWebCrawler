import requests
from bs4 import BeautifulSoup
import pyfiglet
import time
import random
from urllib.parse import urljoin, urlparse

# ASCII art header
ascii_banner = pyfiglet.figlet_format("Spider-Crawl")
print(ascii_banner)

print("# USAGE WARNING: \n# ANY USE OF THIS CODE IS THE SOLE RESPONSIBILITY OF THE USER. \n# This program can cause websites to crash or your IP address to be banned. \n# Please do not use it for fun. \n# Only use it after obtaining permission from the website owners and set the speed to level 3.")

# Function to get target URL from user
def get_target_url():
    while True:
        url = input("Please enter the target URL (e.g., https://www.example.com): ")
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print("Successfully connected to the site.")
                return url
            else:
                print(f"Cannot connect to the site. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"Invalid URL or cannot connect to the site. Error: {e}")

# Function to get crawling speed from user
def get_crawl_speed():
    while True:
        speed = input("Please select crawling speed level (1, 2, or 3): ")
        if speed in ['1', '2', '3']:
            return int(speed)
        else:
            print("Invalid input. Please enter 1, 2, or 3.")

# Target URL
target_url = get_target_url()
crawl_speed = get_crawl_speed()
found_links = []

# Function to get the source code of a URL
def get_source(url):
    try:
        response = requests.get(url)
        source = BeautifulSoup(response.text, "html.parser")
        return source
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching URL: {e}")
        return None

# Recursive function to crawl the website
def crawl(url):
    links = get_source(url)
    if links:
        for link in links.find_all('a', href=True):
            href = link.get('href')
            
            # Convert relative URLs to absolute URLs
            full_url = urljoin(target_url, href)

            # Clean the URL
            parsed_url = urlparse(full_url)
            clean_url = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

            if target_url in clean_url and clean_url not in found_links:
                found_links.append(clean_url)
                print("Found URL: " + clean_url)

                # Add a random delay based on selected speed
                if crawl_speed == 1:
                    delay = random.uniform(0, 1)
                elif crawl_speed == 2:
                    delay = random.uniform(1, 3)
                elif crawl_speed == 3:
                    delay = random.uniform(3, 5)
                time.sleep(delay)

                crawl(clean_url)

crawl(target_url)
