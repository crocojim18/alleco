import scrapy, re
from alleco.objects.official import Official

class ross_t(scrapy.Spider):
	name = "ross_t"
	muniName = "ROSS"
	muniType = "TOWNSHIP"
	complete = True

	def start_requests(self):
		urls = ['https://www.ross.pa.us/245/Board-of-Commissioners',
		'https://www.ross.pa.us/225/Other-Elected-Officials']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-2]=='r':
			for quote in response.xpath('//div[@class="cpTabPanels"]'):
				arr = [i.strip() for i in quote.xpath('.//text()').getall() if len(i.strip())>0 and '$' not in i]
				for i in range(9):
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="COMMISSIONER",
						district=arr[i*4].upper(),
						name=self._name(arr[i*4+1]),
						email=arr[i*4+3],
						url=response.url)
		elif response.url[-2]=='l':
			for quote in response.xpath('//div[contains(h2/text(),"Ross Tax Collector")]/p[1]'):
				yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="TAX COLLECTOR",
						name=quote.xpath('text()[1]').get(),
						email=quote.xpath('a/@href').get(),
						phone=quote.xpath('text()[2]').get(),
						url=response.url)

	def _name(self,string):
		return string.split(",")[0][13:]