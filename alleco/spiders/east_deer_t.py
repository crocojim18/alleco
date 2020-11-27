import scrapy, re
from alleco.objects.official import Official

class east_deer_t(scrapy.Spider):
	name = "east_deer_t"
	muniName = "EAST DEER"
	muniType = "TOWNSHIP"
	complete = False

	def start_requests(self):
		urls = ['http://eastdeertownship.org/commissioners/',
		'http://eastdeertownship.org/tax-collector/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if "commissioners" in response.url:
			for quote in response.xpath('//h3[contains(text(),"Commissioner")]'):
				name = quote.xpath("text()").get()[12:]
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="COMMISSIONER",
					name=name,
					district=self._district(name),
					url=response.url)
		elif "tax" in response.url:
			for quote in response.xpath('//div[contains(p/strong/text(),"Tax Collector")]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath("p[1]/text()").get(),
					phone=quote.xpath("p[2]/text()").get(),
					address=" ".join(quote.xpath("p[4]/text()").get().split(" ")[-3:])+", Pittsburgh, PA 15238",
					url=response.url)
		## INCOMPLETE
		## EXPECTED: 3 AUDITORS, unable to be found on site

	#Ideally this would be scraped from the website itself
	def _district(self,name):
		if "Kissel" in name: return "WARD 2"
		elif "Novosat" in name: return "WARD 1"
		else: return "AT-LARGE"