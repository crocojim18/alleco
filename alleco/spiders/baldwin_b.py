import scrapy
from alleco.objects.official import Official

class baldwin_b(scrapy.Spider):
	name = "baldwin_b"
	muniName = "BALDWIN"
	muniType = "BOROUGH"

	def start_requests(self):
		urls = ['https://www.baldwinborough.org/148/Borough-Council',
		'https://www.baldwinborough.org/155/Property-Taxes']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-1] == "l":
			counter = 1
			for quote in response.xpath('//div[@id="cityDirectoryWidget3e4ca0ff-5ed1-4ca6-86bc-f4ebc4b5ed38"]//ol/li'):
				if counter==1:
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="MAYOR",
						name=quote.xpath("h4/text()").get(),
						email=quote.xpath('div[2]/a/text()').get(),
						url=response.url,
						phone=quote.xpath('div[3]/text()').get().split(": ")[1])
				else:
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="MEMBER OF COUNCIL",
						name=quote.xpath("h4/text()").get(),
						email=quote.xpath('div[2]/a/text()').get(),
						url=response.url)
				counter += 1
		else:
			for quote in response.xpath('//div[@id="cityDirectoryWidgetba8decb7-37d2-4a77-9496-5d8ce39b7341"]/ol/li[1]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath("h4/text()").get(),
					url=response.url,
					phone=quote.xpath('div[2]/text()').get().split(" ")[1])
