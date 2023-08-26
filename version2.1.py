from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import pandas as pd
import time

website = "https://www.eenadu.net/"
path = '/Users/neerajshukla/Downloads/chromedriver_mac_arm64'
path1 = '/Users/PycharmProjects/Web scrapper bot/chromedriver'


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

    headline = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[4]/div[1]/div[1]/h1').text

    timestamp_current = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[4]/div[1]/div[2]/div[1]/span').text
    detail = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[4]/div[1]/div[4]').text

    image = driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[2]/div[4]/div[1]/div[4]/p[1]/img').get_attribute(
        'src')

    if timestamp_current in timestamp:
        print("No Update till now")
    else:
        headlines.append(headline)
        timestamp.append(timestamp_current)
        details.append(detail)
        images.append(image)

    driver.quit()

    new_data = list(zip(headlines, timestamp, details, images))

    # Append new data to the existing CSV file
    if new_data:
        df = pd.DataFrame(new_data, columns=['Headline', 'Time', 'Detail', 'images'])
        if not pd.Series(df.columns).isin(pd.read_csv('/Users/neerajshukla/PycharmProjects/Web scrapper bot/news.csv').columns).all():
            df.to_csv('/Users/neerajshukla/PycharmProjects/Web scrapper bot/news.csv', mode='a', header=False, index=False)
        else:
            df.to_csv('/Users/neerajshukla/PycharmProjects/Web scrapper bot/news.csv', mode='a', header=True, index=False)

# Run the scraping function every 2 minutes
while True:
    scrape_and_save()
    time.sleep(60)  # 120 seconds = 2 minutes

df.to_csv('/Users/neerajshukla/PycharmProjects/Web scrapper bot/news.csv', index=False)

