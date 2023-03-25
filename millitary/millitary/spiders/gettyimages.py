import scrapy
import millitary.util as util
from time import sleep
from scrapy_selenium import SeleniumRequest
from scrapy.selector import Selector
from selenium.webdriver.common.by import By

class GettyimagesSpider(scrapy.Spider):
    name = "gettyimages"
    allowed_domains = ["gettyimages.com"]
    start_urls = ["https://gettyimages.com/"]

    def __init__(self, search_term=None, page_number=None, browser=None, **kwargs):
        # 设置搜索关键词
        self.search_term = search_term
        self.page_number = page_number
        self.driver = util.get_web_driver(browser)
        
        super().__init__(**kwargs)

    def start_requests(self):
        # 模拟搜索操作
        url = f'https://gettyimages.com/photos/{self.search_term}'
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
        while page > 0:
            page_source = driver.page_source
            selector = Selector(text=page_source)
            images = selector.xpath("//img")
            for image in images:
                src = image.xpath("@src").get()
                if src and "https://media.gettyimages.com/" in src:
                    image_urls.append(src)
            button = driver.find_element(By.XPATH, "//button[@data-testid='pagination-button-next' and @type='button']")
            driver.execute_script("arguments[0].click();", button)
            sleep(3)
            page -= 1
        driver.quit()

        for image_url in image_urls:
            util.download_image(image_url, self.search_term, timeout=10)
    
