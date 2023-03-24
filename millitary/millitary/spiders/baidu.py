import scrapy
import requests
import os
import shutil
import re
from selenium import webdriver
from selenium.webdriver.safari.options import Options as SafariOptions
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep


os.environ['WDM_LOCAL'] = '1'

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = ["https://baidu.com/"]

    def __init__(self, search_term=None, page_number=None, browser=None, **kwargs):
        # 设置搜索关键词
        self.search_term = search_term
        self.page_number = page_number
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            self.driver = webdriver.Chrome(chrome_options=options)
        if browser == 'firefox':
            options = webdriver.FirefoxOptions()
            options.add_argument('-headless')
            self.driver = webdriver.Firefox(options=options)
        if browser == 'edge':
            options = webdriver.EdgeOptions()
            options.add_argument('--headless=new')
            options.add_argument('--start-maximized')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            self.driver = webdriver.Edge(options=options)
        if browser == 'safari':
            options = SafariOptions()
            self.driver = webdriver.Safari(options=options)
        
        super().__init__(**kwargs)

    def start_requests(self):
        # 模拟搜索操作
        url = "https://image.baidu.com"
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            meta={'driver': self.driver},
            wait_time=10
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.get(response.url)
        keyword = self.search_term
        search_box = driver.find_element(By.XPATH, "//input[@name='word']")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        pattern = r"https://img\d+.baidu.com"
        page = int(self.page_number)
        image_urls = []
        image_num = 0
        if not os.path.exists(f"images/{self.search_term}"):
                os.makedirs(f"images/{self.search_term}")
        while page > 0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            page -= 1
            if page == 0:
                break
        page_source = driver.page_source
        selector = Selector(text=page_source)
        images = selector.xpath("//img")
        for image in images:
            src = image.xpath("@src").get()
            if src and re.search(pattern, src):
                image_urls.append(src)
        driver.quit()

        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15'
        }
        for image_url in image_urls:
            image_response = requests.get(image_url, headers=headers, stream=True)
            file_name = f'image_{image_num}.jpg' 
            file_name = os.path.join(f"images/{self.search_term}", file_name)
            with open(file_name, "wb") as f:
                shutil.copyfileobj(image_response.raw, f)
            image_num += 1
    
