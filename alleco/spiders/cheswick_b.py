import scrapy
from alleco.objects.official import Official

class cheswick_b(scrapy.Spider):
	name = "cheswick_b"
	muniName = "CHESWICK"
	muniType = "BOROUGH"
	complete = False

	def start_requests(self):
		urls = ['https://www.cheswick.us/info']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//div[@class="default-text"]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=" ".join(quote.xpath("text()[10]").get().split(".")[2].split(" ")[-2:]),
				phone=quote.xpath("text()[10]").get().split(".")[6].split(" ")[-1],
				url=response.url)
	#### Additional Expected positions: 1 mayor, 7 members of council at-large
	#### Unable to be found on their website