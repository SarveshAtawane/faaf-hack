from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

def scrape_google_maps_results(search_query: str):
    # Create Chrome options
    options = Options()
    options.add_argument('--headless')  # Set to False if you want to see the browser
    options.add_argument('--window-size=1920,1080')
    driver = webdriver.Chrome(options=options)

    # Construct URL
    search_url = f"https://www.google.com/maps/search/{search_query.replace(' ', '+')}"
    print(f"Opening: {search_url}")
    driver.get(search_url)

    time.sleep(5)  # Wait for the results to load

    # Find result containers on the left-hand panel
    results = driver.find_elements(By.CSS_SELECTOR, '.hfpxzc')
    print(f"\nFound {len(results)} vendors:\n{'='*60}")

    for i, res in enumerate(results, 1):
        try:
            name = res.find_element(By.CSS_SELECTOR, '.qBF1Pd').text
        except:
            name = "N/A"
        try:
            rating = res.find_element(By.CSS_SELECTOR, '.MW4etd').text
        except:
            rating = "N/A"
        try:
            address = res.find_element(By.CSS_SELECTOR, '.W4Efsd').text
        except:
            address = "N/A"

        print(f"{i}. {name}")
        print(f"   Rating: {rating}")
        print(f"   Address: {address}\n")

    driver.quit()

# Example usage
scrape_google_maps_results("laptop repair in Nashik")
