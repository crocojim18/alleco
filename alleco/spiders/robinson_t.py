import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class robinson_t(scrapy.Spider):
	name = "robinson_t"
	muniName = "ROBINSON"
	muniType = "TOWNSHIP"
	complete = True

	def start_requests(self):
		urls = ['https://townshipofrobinson.com/commissioners/',
		'https://townshipofrobinson.com/real-estate-tax/']
		for url in urls:
			yield scrapy.Request(url=url,
				callback=self.parse,
				headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
				})

	def parse(self, response):
		if 'commissioners' in response.url:
			for quote in response.xpath('//h4[contains(text(),"Township Commissioners")]/../div'):
				bits = getAllText(quote)
				for person in range(len(bits)//4):
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="COMMISSIONER",
						name=bits[person*4],
						email=bits[person*4+3],
						url=response.url)
		elif 'tax' in response.url:
			for quote in response.xpath('//h4[contains(text(),"Tax Collector")]/../div'):
					bits = getAllText(quote)
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="TAX COLLECTOR",
						name=bits[0],
						phone=bits[2],
						email=bits[3],
						url=response.url)
