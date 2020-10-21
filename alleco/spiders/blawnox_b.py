import scrapy
from alleco.objects.official import Official

class blawnox_b(scrapy.Spider):
	name = "blawnox_b"
	muniName = "BLAWNOX"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['https://www.blawnox.com/borough-mayor-council',
				'https://www.blawnox.com/tax-collector']
		for url in urls:
			yield scrapy.Request(url=url, 
				callback=self.parse, 
				headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
				})

	def parse(self, response):
		if response.url[-1] == "l":
			counter = 0
			for quote in response.xpath('//table[@class="views-table cols-2"]/tbody/tr'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR" if counter==0 else "MEMBER OF COUNCIL",
					name=" ".join(quote.xpath("td[1]//text()").getall()),
					url=response.url)
				counter += 1
		else:
			bits = [x.strip() for x in response.xpath('//div[@class="adr"]//text()').getall() if len(x.strip())>1][1:5]
			bits[0] = bits[0]+","
			bits[1] = bits[1]+","
			for quote in response.xpath('//tr[@class="odd views-row-first views-row-last"]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					address=" ".join(bits),
					office="TAX COLLECTOR",
					name=quote.xpath("td[1]/a/text()").get(),
					phone=quote.xpath("td[3]/text()").get(),
					url=response.url)
