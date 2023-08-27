from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time
import os

website = "https://www.eenadu.net/"
path = '/Users/neerajshukla/Downloads/chromedriver_mac_arm64'
csv_path = '/Users/neerajshukla/PycharmProjects/Web scrapper bot/news.csv'

def scrape_and_save():
    headlines = []
    details = []
    images = []
    timestamp = []

    driver = webdriver.Chrome()
    driver.get(website)

    wait = WebDriverWait(driver, 60)
    button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="wrapper"]/div[3]/div[2]/ul/li[1]/p/a')))
    button.click()

    # ... Your scraping logic ...

    driver.quit()

    new_data = list(zip(headlines, timestamp, details, images))

    # Load existing data from CSV file if it exists
    if os.path.exists(csv_path):
        existing_data = pd.read_csv(csv_path)
    else:
        existing_data = pd.DataFrame()

    # Convert existing data to a set of tuples for easy comparison
    existing_set = {tuple(row) for row in existing_data.values}

    # Append new data to the existing data if it's not a duplicate
    data_to_append = [row for row in new_data if tuple(row) not in existing_set]

    if data_to_append:
        df_to_append = pd.DataFrame(data_to_append, columns=['Headline', 'Time', 'Detail', 'images'])
        mode = 'a' if os.path.exists(csv_path) else 'w'  # Use 'w' if file is being created
        df_to_append.to_csv(csv_path, mode=mode, header=not os.path.exists(csv_path), index=False)

# Run the scraping function every 2 minutes
while True:
    scrape_and_save()
    time.sleep(120)  # 120 seconds = 2 minutes
