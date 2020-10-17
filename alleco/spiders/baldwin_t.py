import scrapy
from alleco.objects.official import Official

class baldwin_t(scrapy.Spider):
	name = "baldwin_t"
	muniName = "BALDWIN"
	muniType = "TOWNSHIP"

	def start_requests(self):
		urls = ['https://baldwintownship.com/officials.html']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//div[@class="baldwin-staff"]//strong[contains(text(),"Board ")]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="COMMISSIONER",
				name=quote.xpath("../h4/text()").get(),
				url=response.url)
		for quote in response.xpath('//div[contains(strong/text(),"Taxes")]/h4'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=quote.xpath("text()").get(),
				url=response.url)
