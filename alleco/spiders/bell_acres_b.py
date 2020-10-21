import scrapy, re
from alleco.objects.official import Official

class bell_acres_b(scrapy.Spider):
	name = "bell_acres_b"
	muniName = "BELL ACRES"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['http://bellacresborough.org/government/',
		'http://bellacresborough.org/borough-services/taxes/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-2] == "t":
			for quote in response.xpath('//article[@id="post-28"]/div/p[2]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=quote.xpath("text()").get(),
					url=response.url)
			for quote in response.xpath('//article[@id="post-28"]/div/p[1]/text()').getall():
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=quote.split("–")[0],
					url=response.url)
		else:
			for quote in response.xpath('//article[@id="post-129"]/div/p[3]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath('strong/text()').get(),
					email=quote.xpath('a/text()').get(),
					phone=quote.xpath('./text()').getall()[2].split(": ")[1],
					address=", ".join([x.strip() for x in quote.xpath('./text()').getall()[0:2]]),
					url=response.url)
