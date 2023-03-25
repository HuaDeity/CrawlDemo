import scrapy
import millitary.util as util
from time import sleep
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BaiduSpider(scrapy.Spider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = ["https://baidu.com/"]

    def __init__(self, search_term=None, image_number=None, browser=None, **kwargs):
        # 设置搜索关键词
        self.search_term = search_term
        self.image_number = image_number
        self.driver = util.get_web_driver(browser)
        
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='word']"))
        )
        search_box = driver.find_element(By.XPATH, "//input[@name='word']")
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.ENTER)
        sleep(3)
        image = int(self.page_number)
        image_urls = []

        element = driver.find_element(By.CSS_SELECTOR, 'img.main_img')
        element.click()
        window_handles = driver.window_handles
        driver.switch_to.window(window_handles[-1])
        sleep(3)
        last_src = ""
        while image > 0:
            img = driver.find_element(By.CLASS_NAME, 'img-container').find_element(By.TAG_NAME, 'img')
            src = img.get_attribute('src')
            while last_src == src:
                src = img.get_attribute('src')
            last_src = src
            image_urls.append(src)
            image -= 1
            driver.find_element(By.CLASS_NAME, 'img-next').click()
        driver.quit()

        for image_url in image_urls:
            util.download_image(image_url, self.search_term, timeout=10)
