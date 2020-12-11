import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class ingram_b(scrapy.Spider):
	name = "ingram_b"
	muniName = "INGRAM"
	muniType = "BOROUGH"
	complete = False

	def start_requests(self):
		urls = ['https://www.ingramborough.org/mayor-borough-council']
		for url in urls:
			yield scrapy.Request(url=url, 
				callback=self.parse, 
				headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
				})

	def parse(self, response):
		if "council" in response.url:
			for quote in response.xpath('//tbody/tr'):
				bits = getAllText(quote)
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR" if bits[1]=="Mayor" else "MEMBER OF COUNCIL",
					name=bits[0],
					email=bits[3],
					termEnd=bits[2],
					url=response.url)
		##EXPECTED: 1 tax collector
		## It may be Lorraine Rehtoric given section 8(h)
		##in the September 14, 2020 agenda of the borough council