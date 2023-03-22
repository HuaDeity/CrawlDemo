import scrapy
import requests
import os
import shutil
import base64
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

class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]
    start_urls = ["https://google.com/"]

    def __init__(self, search_term=None, page_number=None, browser=None, **kwargs):
        # 设置搜索关键词
        self.search_term = search_term
        self.page_number = page_number
        if browser == "chrome":
            options = webdriver.ChromeOptions()
            # options.add_argument('--headless=new')
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
        url = "https://google.com/imghp"
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
        search_box = driver.find_element(By.XPATH, "//input[@name='q']")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        page = int(self.page_number)
        image_urls = []
        image_num = 0
        while page > 0:
        		page_source = driver.page_source
            selector = Selector(text=page_source)
            images = selector.xpath("//img[@class='rg_i Q4LuWd']")
			for image in images:
				src = image.xpath("@src").get()
				if src and "https://" in src:
         			image_urls.append(src)
                elif src and "data:image/jpeg;base64" in src:
            			base64.b64decode(src.split(','[-1]))
                    file_name = f'image_{image_num}.jpg' 
                    file_name = os.path.join(f"images/{self.search_term}", file_name)
                    with open(file_name, "wb") as f:
                    		f.write(decoded_data)
                    image_num += 1
			last_height=driver.execute_script("return document.body.scrollHeight;")
			driver.execute_script("window.scrollTo(0, {last_height});")
            # 获取当前滚动的高度
         	# current_scroll_height = driver.execute_script("return window.pageYOffset || document.documentElement.scrollTop;")
            # 如果滚动到了屏幕底部，就退出循环
            # if current_scroll_height + window_height >= driver.execute_script("return document.body.scrollHeight;") - 30:
            #		break
            # 否则，就继续逐行滚动
            #else:
            	#	driver.execute_script(f"window.scrollBy(0, {window_height});")
				
        driver.quit()

        if not os.path.exists(f"images/{self.search_term}"):
                os.makedirs(f"images/{self.search_term}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15'
        }
        for image_url in image_urls:
            image_response = requests.get(image_url, headers=headers, stream=True)
            file_name = f'image_{image_num}.jpg' 
            file_name = os.path.join(f"images/{self.search_term}", file_name)
            with open(file_name, "wb") as f:
                shutil.copyfileobj(image_response.raw, f)
            file_num += 1
    
