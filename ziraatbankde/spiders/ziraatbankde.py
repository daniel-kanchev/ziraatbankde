import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from ziraatbankde.items import Article


class ZiraatbankdeSpider(scrapy.Spider):
    name = 'ziraatbankde'
    start_urls = ['https://www.ziraatbank.de/de/news']

    def parse(self, response):
        links = response.xpath('//div[@class="list-box-item"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h1/text()').get()
        if title:
            title = title.strip()

        content = response.xpath('//div[@id="ContentSection"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
