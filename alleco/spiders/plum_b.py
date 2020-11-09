import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class plum_b(scrapy.Spider):
	name = "plum_b"
	muniName = "PLUM"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['https://www.plumboro.com/government',
		'https://www.plumboro.com/finance/pages/real-estate-tax']
		for url in urls:
			yield scrapy.Request(url=url, 
				callback=self.parse, 
				headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
				})

	def parse(self, response):
		if response.url[-1]=='t':
			for quote in response.xpath('//table[@class="views-table cols-3"]/tbody/tr'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR" if quote.xpath("td[2]/text()").get().strip()=="Mayor" else "MEMBER OF COUNCIL",
					name=quote.xpath("td[1]/a/text()").get(),
					phone=quote.xpath("td[3]/text()").get(),
					url=response.url)
		elif response.url[-1]=='x':
			for quote in response.xpath('//div[contains(h5/text(),"Real Estate Property Tax")]/p[3]'):
				text = getAllText(quote)
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=text[0].split(",")[0],
					phone=text[3],
					address=text[1]+", "+text[2],
					url=response.url)
