import scrapy
import requests
import os
import shutil
from selenium import webdriver
from selenium.webdriver.safari.options import Options as SafariOptions
from selenium.webdriver.common.action_chains import ActionChains
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

os.environ['WDM_LOCAL'] = '1'

class AlamySpider(scrapy.Spider):
    name = "alamy"
    allowed_domains = ["alamy.com"]
    start_urls = ["https://alamy.com/stock-photo/"]

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
        url = f'https://alamy.com/stock-photo/{self.search_term}.html'
        yield SeleniumRequest(
            url=url,
            callback=self.parse,
            meta={'driver': self.driver},
            wait_time=10
        )

    def parse(self, response):
        driver = response.meta['driver']
        driver.get(response.url)
        page = int(self.page_number)
        image_urls = []
        # 获取浏览器窗口高度
        window_height = driver.execute_script("return window.innerHeight;")
        while page > 0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(20)
            page_source = driver.page_source
            selector = Selector(text=page_source)
            images = selector.xpath("//img")
            for image in images:
                src = image.xpath("@src").get()
                if src and "https://h7.alamy.com/" in src:
                    image_urls.append(src)
            button = driver.find_element(By.XPATH, "//a[@data-testid='pagination-next-page']")
            driver.execute_script("arguments[0].click();", button)
            sleep(3)
            page -= 1
        driver.quit()

        if not os.path.exists(f"images/{self.search_term}"):
                os.makedirs(f"images/{self.search_term}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15'
        }
        for image_url in image_urls:
            image_response = requests.get(image_url, headers=headers, stream=True)
            file_name = image_url.split("/")[-1].split("?")[0]
            file_name = os.path.join(f"images/{self.search_term}", file_name)
            with open(file_name, "wb") as f:
                shutil.copyfileobj(image_response.raw, f)
    
