import scrapy

from scrapy.loader import ItemLoader

from ..items import FirstpremierItem
from itemloaders.processors import TakeFirst


class FirstpremierSpider(scrapy.Spider):
	name = 'firstpremier'
	start_urls = ['https://www.firstpremier.com/en/pages/about-us/press-room/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="col-md-12"]')
		for post in post_links:
			url = post.xpath('.//p[@class="col-md-9"]/a/@href').get()
			title = post.xpath('.//p[@class="col-md-9"]/a/text()').get()
			date = post.xpath('.//span[@class="col-md-3"]/text()').get()
			if url:
				yield response.follow(url, self.parse_post, cb_kwargs={'date': date, 'title': title})

	def parse_post(self, response, date, title):
		description = response.xpath('//div[@class="xhtml"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()

		item = ItemLoader(item=FirstpremierItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
