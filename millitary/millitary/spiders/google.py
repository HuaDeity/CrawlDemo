from time import sleep
from urllib.parse import unquote

import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import millitary.util as util


class GoogleSpider(scrapy.Spider):
    name = "google"
    allowed_domains = ["google.com"]
    start_urls = ["https://google.com/"]

    def __init__(self, search_term=None, page_number=None, browser=None, **kwargs):
        # 设置搜索关键词
        self.search_term = search_term
        self.page_number = page_number
        self.driver = util.get_web_driver(browser)
        
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//textarea"))
        )
        search_box = driver.find_element(By.XPATH, "//textarea")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        sleep(3)
        page = int(self.page_number)
        image_urls = []
        
        while page > 0:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(3)
            page -= 1
            if page == 0:
                break
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.XPATH, "//*[contains(@class, 'islib nfEiy')]")
            )
        )
        for i, element in enumerate(elements):
            try:
                element.click()
            except Exception:
                continue
            encoded_url = element.get_attribute("href")
            try:
                decoded_url = unquote(encoded_url)
                src = decoded_url.split('imgurl=')[1].split('&')[0]
                image_urls.append(src)
            except Exception:
                continue
        driver.quit()

        for image_url in image_urls:
            util.download_image(image_url, self.search_term, timeout=10)
