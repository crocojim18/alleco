import scrapy
from alleco.objects.official import Official

class ben_avon_b(scrapy.Spider):
	name = "ben_avon_b"
	muniName = "BEN AVON"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['https://benavon.com/ben-avon-2/',
		'https://benavon.com/taxes-utilities/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-2] == "2":
			for quote in response.xpath('//div[@id="panel-2-0-1-0"]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=quote.xpath("h3/text()").get(),
					email=quote.xpath(".//a/@href").get(),
					url=response.url)
			for quote in response.xpath('//div[@id="pl-2"]/div')[1:8]:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=quote.xpath('div[2]//h3/text()').get(),
					email=quote.xpath('div[2]//a/@href').get(),
					url=response.url)
		elif response.url[-2] == "s":
			for quote in response.xpath('//article[@id="post-291"]/div/p[6]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath("./text()").get(),
					phone=quote.xpath("./text()").getall()[2].strip().split(" ")[1],
					url=response.url)
