import scrapy
from alleco.objects.official import Official

class bridgeville_b(scrapy.Spider):
	name = "bridgeville_b"
	muniName = "BRIDGEVILLE"
	muniType = "BOROUGH"

	def start_requests(self):
		urls = ['https://bridgevilleboro.com/officials/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//p[contains(strong/text(),"Seated:")]/../p[5]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				name=quote.xpath("text()").get(),
				url=response.url)
		for quote in response.xpath('//p[contains(strong/text(),"Seated:")]/../p[29]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=quote.xpath("text()").get(),
				url=response.url)
		for line in range(8, 15):
			for quote in response.xpath('//p[contains(strong/text(),"Seated:")]/../p[{}]'.format(line)):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=quote.xpath("text()").get(),
					url=response.url)