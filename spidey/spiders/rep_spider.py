import scrapy
from scrapy_selenium import SeleniumRequest
from bs4 import BeautifulSoup
from spidey.items import RepItem

class RepSpider(scrapy.Spider):
    name = "rep_spider"
    start_urls = ["https://qa-reps.corenroll.com/login"]
    custom_settings = {
        "DOWNLOAD_DELAY": 2,
    }

    async def start(self):
        yield SeleniumRequest(
            url=self.start_urls[0],
            callback=self.parse_login,
            wait_time=10,
            wait_until=lambda driver: driver.find_element("name", "username")
        )


    def parse_login(self, response):
        driver = response.meta.get("driver")
        if driver:
            user_field = driver.find_element_by_name("Email")
            user_field = driver.find_element_by_name("password")
            user_field.send_keys("email")
            pass_field.send_keys("passwd")
            driver.find_element_by_name("login").click()
            self.logger.info("logged in, now accesing protected page")
            html = driver.page_source
            response = scrapy.Selector(text=html)
            
        for href in response.css("a.rep_detail::attr(href)").getall():
            yield response.follow(href, callback=self.parse_rep)

        
    def parse_rep(self, response):
        item = RepItem()
        item['name'] = response.css("h1.rep-name::text").get().strip()
        item['rep_id'] = response.css("p.rep_id::text").get()

        soup = BeautifulSoup(response.text, "html.parser")
        phone = soup.find("span", {"class": "phone"})
        item['phone'] = phone.get_text(strip=true) if phone else None
        email = soup.find("a", {"class": "email"})
        item['email'] = email.get_text(strip=true) if email else None
        yield item