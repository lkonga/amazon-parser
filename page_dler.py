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

# Use the function
html = download_page('https://www.amazon.com/Natures-Valley-granola-Crunchy-Honey/dp/B0025W9A5C/ref=sr_1_2?sr=8-2')
with open('output.html', 'w') as f:
    f.write(html)
