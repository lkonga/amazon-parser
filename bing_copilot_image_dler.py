import os
import sys
import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from parsel import Selector


def download_page(url, image_num):
    try:
        # Set up a headless Chrome browser
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=options)

        # Navigate to the page
        driver.get(url)

        # Get the HTML of the page
        html = driver.page_source

        # Parse the HTML with Parsel
        selector = Selector(html)

        # Find the image element
        image_elem = selector.xpath(
            '//div[contains(@class, "mainImage")]/div/div/div/img')

        # Get the image URL
        image_url = image_elem.xpath('./@src').get()

        if image_url is None:
            print(f"No image found on {url}")
            return html

        # Download the image
        response = requests.get(image_url)

        # Get the directory of the script file
        script_dir = os.path.dirname(os.path.realpath(__file__))

        # Create the directory if it doesn't exist
        os.makedirs(os.path.join(script_dir, 'copilot_images'), exist_ok=True)

        # Save the image
        with open(os.path.join(script_dir, f'copilot_images/image{image_num}.jpg'), 'wb') as file:
            file.write(response.content)
    except Exception as e:
        print(f"An error occurred while processing {url}: {e}")
    finally:
        # Close the browser
        driver.quit()

    return html


# Read the URLs from the input file
with open('urls_copilot_images.txt', 'r') as file:
    urls = file.readlines()

# Download the pages and images
for i, url in enumerate(urls, start=1):
    download_page(url.strip(), i)
