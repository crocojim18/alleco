import scrapy
from alleco.objects.official import Official

class castle_shannon_b(scrapy.Spider):
	name = "castle_shannon_b"
	muniName = "CASTLE SHANNON"
	muniType = "BOROUGH"

	def start_requests(self):
		urls = ['https://borough.castle-shannon.pa.us/resources/government-officials/',
		'https://borough.castle-shannon.pa.us/administration/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-2] == 's':
			for quote in response.xpath('//div[@class="cs-program-content"]/ul/li'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=quote.xpath("text()").get().split(",")[0],
					url=response.url)
		elif response.url[-2]=='n':
			phone=response.xpath('//p[contains(text(),"Fax")]/text()').getall()[1][5:]
			for quote in response.xpath('//h2[contains(text(),"Borough Administration")]/../p')[2:4]:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office=quote.xpath("text()").getall()[0].upper(),
					name=quote.xpath("text()").getall()[1],
					phone=phone+" ".join(quote.xpath("text()").getall()[2].split(" ")[:2]),
					url=response.url)
