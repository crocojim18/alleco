import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class pennsbury_village_b(scrapy.Spider):
	name = "pennsbury_village_b"
	muniName = "PENNSBURY VILLAGE"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['http://pennsburyvillageboro.com/government/']
		for url in urls:
			yield scrapy.Request(url=url, 
				callback=self.parse, 
				headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
				})

	def parse(self, response):
		addressSuffix = ", Pittsburgh, PA 15205"
		for quote in response.xpath('//div[@class="pf-content"]/p[1]'):
			mayorBits = getAllText(quote)
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				name=mayorBits[1],
				url=response.url,
				address=mayorBits[2]+addressSuffix,
				phone=mayorBits[3])
		for quote in response.xpath('//div[@class="pf-content"]/table/tbody/tr'):
			memberBits = getAllText(quote)
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MEMBER OF COUNCIL",
				name=memberBits[0].split("–")[0],
				url=response.url,
				address=memberBits[1]+addressSuffix,
				phone=memberBits[2])
		for quote in response.xpath('//div[@class="pf-content"]/p[5]'):
			taxBits = getAllText(quote)
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=taxBits[1],
				url=response.url,
				email=taxBits[2],
				phone=taxBits[3])
