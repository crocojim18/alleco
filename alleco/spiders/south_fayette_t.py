import scrapy, re
from alleco.objects.official import Official

class south_fayette_t(scrapy.Spider):
	name = "south_fayette_t"
	muniName = "SOUTH FAYETTE"
	muniType = "TOWNSHIP"
	complete = True

	def start_requests(self):
		urls = ['https://southfayettepa.com/185/Board-of-Commissioners',
		'https://southfayettepa.com/259/Real-Estate-Taxes']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-2]=='r':
			for quote in response.xpath('//li[@class="widgetItem h-card"]')[0:5]:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="COMMISSIONER",
					email=quote.xpath("div[2]/a/@href").get(),
					name=quote.xpath("h4/text()").get(),
					url=response.url)
		elif response.url[-2]=='e':
			for quote in response.xpath('//li[@class="InfoAdvanced widgetItem "]')[0:1]:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath('h3[1]/text()').get(),
					address=quote.xpath('text()[7]').get().strip()+", "+quote.xpath('text()[8]').get().strip(),
					phone=quote.xpath('div[1]/text()').get(),
					url=response.url)
