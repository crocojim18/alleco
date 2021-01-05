import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class elizabeth_t(scrapy.Spider):
	name = "elizabeth_t" # name of spider
	muniName = "ELIZABETH" # name of municipality
	muniType = "TOWNSHIP" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["http://www.elizabethtownshippa.com/board-of-commissioners",
		"http://www.elizabethtownshippa.com/tax-collector"] # urls for requests go here
		for url in urls:
			yield scrapy.Request(url=url,callback=self.parse)

	def parse(self, response):
		if "tax" in response.url:
			for quote in response.xpath("//div[p/text()='Tax Collector']/.."):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath("div[2]/h1/span/span/span/text()").get(),
					phone=quote.xpath("div[4]/p/text()").get(),					
					url=response.url)
		elif "commissioners" in response.url:
			for quote in response.xpath("//p[contains(text(),'Ward ')]/../.."):
				allText = getAllText(quote)
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="COMMISSIONER",
					name=allText[0],
					email=allText[1],
					phone=allText[2],
					district=allText[3].upper(),					
					url=response.url)
