import requests
import os
import shutil
from urllib.parse import unquote
from selenium import webdriver
from selenium.webdriver.safari.options import Options as SafariOptions

def get_web_driver(browser):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Chrome(chrome_options=options)
    elif browser == 'firefox':
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
    elif browser == 'edge':
        options = webdriver.EdgeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        driver = webdriver.Edge(options=options)
    elif browser == 'safari':
        options = SafariOptions()
        driver = webdriver.Safari(options=options)
    return driver
     

def download_image(image_url, search_term, timeout=10):
    try:
        if not os.path.exists(f"images/{search_term}"):
                os.makedirs(f"images/{search_term}")
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15'}
        image_response = requests.get(image_url, headers=headers, stream=True, timeout=timeout)
        image_url = unquote(image_url)
        file_name = image_url.split("/")[-1].split("?")[0].strip()
        if len(file_name) == 0:
            return False
        name, ext = os.path.splitext(file_name)
        if not ext:
            file_name = f"{name}.jpg"
        file_name = os.path.join(f"images/{search_term}", file_name)
        with open(file_name, "wb") as f:
            shutil.copyfileobj(image_response.raw, f)
        return True
    except Exception:
        return False