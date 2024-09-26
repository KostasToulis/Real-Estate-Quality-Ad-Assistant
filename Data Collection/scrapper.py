# import requests
# from bs4 import BeautifulSoup
import json
import os
import time
import random
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

headers_list = [
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'},
    {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36'},
    {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"},
    {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"}
]

ua = UserAgent()
SCRAPERAPI_KEY = '61fe3ef9e47317068b6125cafccfad12'


def get_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")
    # chrome_options.add_argument(f"user-agent={random.choice(headers_list)['User-Agent']}")
    chrome_options.add_argument(f"user-agent={ua.random}")
    proxy = f"http://scraperapi:{SCRAPERAPI_KEY}@proxy-server.scraperapi.com:8001"
    # chrome_options.add_argument(f'--proxy-server={proxy}')

    # i = random.randint(0,2)

    # if i == 0:
    driver = webdriver.Chrome(options=chrome_options)
    # if i == 1:
    # driver = webdriver.Firefox(options=chrome_options)
    # if i == 2:
    # driver = webdriver.Edge(options=chrome_options)


    return driver


def simulate_human_interaction(driver):
    actions = ActionChains(driver)
    for _ in range(random.randint(1, 3)):
        actions.move_by_offset(random.randint(0, 10), random.randint(0, 10)).perform()
        time.sleep(random.uniform(0.5, 2))
    driver.execute_script("window.scrollBy(0, {})".format(random.randint(100, 500)))


def scrape_real_estate(urls):
    driver = get_driver()

    for url in urls:
        try:
            # i = random.randint(1,20)
            # if i==5: driver = get_driver()
            driver.get(url)
            cookies_file = 'cookies.json'

            if os.path.exists(cookies_file):
                try:
                    load_cookies(driver, cookies_file)
                    driver.get(url)
                except:
                    print("Could not load cookies")

            time.sleep(random.uniform(2, 5))
            wait = WebDriverWait(driver, 20)

            simulate_human_interaction(driver)

            images = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'property__gallery__item')))

            location = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'property__address'))).text.strip()
            try:
                description = wait.until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'property__description'))).text.strip()
            except:
                description = ""
            price = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'property__price__text'))).text.strip()
            price = fix_price(price)

            image_urls = []

            for image in images:
                try:
                    image_urls.append(image.find_element(By.TAG_NAME, 'img').get_attribute('src'))
                    time.sleep(random.uniform(0.1, 1))
                except Exception as e:
                    print(f"Error extracting data: {e}")
                    continue

            save_cookies(driver, cookies_file)
            description = description.replace('\n', ' ')
            with open("data.txt", 'a', encoding="utf-8") as file:
                file.write(url)
                for image in image_urls:
                    file.write(image + ' ')
                file.write('\n')
                file.write(description + '\n')
                file.write(location + '\n')
                file.write(str(price) + '\n')
                # file.write('\n')
            with open("success.txt", 'a', encoding="utf-8") as file:
                file.write(url)
        except:
            print(url)


def fix_price(price):
    price_fixed = price[1:]
    price_fixed = price_fixed.replace(',', '')
    price_fixed = float(price_fixed)
    return price_fixed


def save_cookies(driver, file_path):
    cookies = driver.get_cookies()
    with open(file_path, 'w') as file:
        json.dump(cookies, file)


def load_cookies(driver, file_path):
    with open(file_path, 'r') as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)


def scrape_url(url):
    image_urls, price, location, description = scrape_real_estate(url)
    description = description.replace('\n', ' ')
    with open("data1.txt", 'a', encoding="utf-8") as file:
        for image in image_urls:
            file.write(image + ' ')
        file.write('\n')
        file.write(description + '\n')
        file.write(location + '\n')
        file.write(str(price) + '\n')
