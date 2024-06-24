import os
import sys
import re
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def download_page(url):
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

    # Close the browser
    driver.quit()

    return html


def test_regex(url, pattern):
    match = pattern.search(url)
    if match:
        print(f"Match found: {match.group(1)}")
    else:
        print("No match found.")


# Create the output directory if it doesn't exist
output_dir = 'pages_html_output'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Check if file path is passed as command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <file_path>")
    sys.exit(1)

# Read the URLs from the file
file_path = sys.argv[1]
with open(file_path, 'r') as f:
    urls = f.read().splitlines()

# Filter and clean URLs
pattern = re.compile(r'(https://www\.amazon\.com/[^/]+/[^/]+/dp/[^/]+)')
pattern = re.compile(r'(https://www\.amazon\.com/[^/]+/[^/]+/dp/[^/]+)')
pattern = re.compile(r'(https://www\.amazon\.com/[^/]+/[^/]+/dp/[^/]+)')
pattern = re.compile(r'(https://www\.amazon\.com/[^/]+/[^/]+/dp/[^/?]+)')
pattern = re.compile(r'(https://www\.amazon\.com/[^/]+/[^/]+/dp/[^/?]+)')


urls = [url.split('/ref')[0] for url in urls if "/dp/" in url]
# Count the number of URLs before removing duplicates
print(f"Number of URLs before removing duplicates: {len(urls)}")

# Remove duplicates
urls = list(set(urls))

# Count the number of URLs after removing duplicates
print(f"Number of URLs after removing duplicates: {len(urls)}")
# Pretty print the resulting URLs
print("Resulting URLs:")
for url in urls:
    print(url)

# urls = [pattern.search(url).group(1) for url in urls if pattern.search(url)]
# urls = list(set(urls))  # Remove duplicates

# Test the regular expression with a sample URL
# test_url = 'https://www.amazon.com/Variety-Potatoes-Vegetable-Turmeric-Chickpea/dp/B0CQD5MNQ5/ref=sr_1_39?crid=19OE0DVVWFL5U&dib=eyJ2IjoiMSJ9.h0oHtBJciXjw6AIeA6cG0K_2rYzhyoqFSDDLClRlNIcT4hBvolyFZ_hN9rimlGsDbyxD2lK-eKmyKzXtIMu-31ZMA1yDQJyzqOUWp3UOwNfC2xfLsxeMznMifVy7EWoSKeTlzTadHrm4Qkf_r6Sflbaxj3UsKu8OlJRJxzt2tvy4XnxQnFZHWvpWHPqSW6xsn1BTT7-LHhVwE8mKSR92acBXy5kAUQ95qUMelfGRkl3o4pL8yAmMxXZs6pVRBOO9knlqRTVF4ks4gTlkzJuKlDGh4LyIBgTvhdvuZqTIXEc.Z8U5pkrH1o0LlDLJLMRNrlqPte9r7Gpf578foKQ97Ak&dib_tag=se&keywords=indian+groceries&qid=1719194561&sprefix=indigroceries%2Caps%2C322&sr=8-39#customerReviews'
# test_regex(test_url, pattern)

# Download each URL
for i, url in enumerate(urls, start=1):
    html = download_page(url)
    # Extract product name from URL and make it lowercase
    product_name = url.split('/')[3].lower()
    with open(f'{output_dir}/{i:04d}-{product_name}.html', 'w') as f:
        f.write(html)
