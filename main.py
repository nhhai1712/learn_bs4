from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import json
# Configure Chrome options
chrome_options = ChromeOptions()
# Run Chrome in headless mode (no GUI)
# chrome_options.add_argument("--headless")

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
chrome_options.add_argument(f'user-agent={user_agent}')
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")

# Set up the Chrome web driver
driver = webdriver.Chrome(service=ChromeService(
    "./chromedriver.exe"), options=chrome_options)

# URL of the web page you want to scrape

data_coin = []
column_names = ["", "ID", "Name", "Price", "1h %", "24h %", "7d %", "Market Cap", "Volumn(24h)", "Circulating Supply"]
for i in range(1,89):
    url = f"https://coinmarketcap.com/?page={i}"
    driver.get(url)
    time.sleep(2)
    # Define the scroll amount and duration for smooth scrolling
    scroll_amount = 500  # Adjust this value as needed
    scroll_duration = 0.0001  # Adjust this value as needed

    # Get the initial height of the page
    initial_height = driver.execute_script("return window.scrollY")
    while True:
        # Scroll down by the defined scroll amount
        driver.execute_script(f"window.scrollBy(0, {scroll_amount});")

        # Wait for a short duration to create a smooth scrolling effect
        time.sleep(scroll_duration)

        # Get the new scroll position
        new_height = driver.execute_script("return window.scrollY")

        # If no further scrolling is possible, break out of the loop
        if new_height == initial_height:
            break

        # Update the initial height
        initial_height = new_height
    # tbody_element = driver.find_element_by_xpath("//tbody")
    tbody_element = driver.find_element(By.XPATH, "//tbody")

    # Find child <tr> elements within the <tbody>
    # tr_elements = tbody_element.find_elements_by_tag_name("tr")
    tr_elements = tbody_element.find_elements(By.TAG_NAME, "tr")
    
    for tr_element in tr_elements:
        # print(tr_element.text)
        td_elements = tr_element.find_elements(By.TAG_NAME, "td")
        row = {}
        for i, td_element in enumerate(td_elements):
            if i < len(column_names):
                column_name = column_names[i]
            else:
                column_name = f"col{i}"
            column_value = td_element.text
            if(td_element.find_elements(By.CLASS_NAME, "icon-Caret-down")):
                column_value = "-" + column_value
            if(td_element.find_elements(By.CLASS_NAME, "icon-Caret-up")):
                column_value = "+" + column_value
            if '\n' in column_value:
                column_value = column_value.replace('\n', ' - ')   
            if column_value.strip() != "":
                row[column_name] = column_value
            
        
        if row:
            data_coin.append(row)

    with open("data_coin.json", "w") as json_file:
        json.dump(data_coin, json_file, indent=4)
driver.close()
    
# Close the Selenium browser