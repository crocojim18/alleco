import scrapy
from alleco.objects.official import Official

class bradford_woods_b(scrapy.Spider):
	name = "bradford_woods_b"
	muniName = "BRADFORD WOODS"
	muniType = "BOROUGH"

	def start_requests(self):
		urls = ['https://www.bradfordwoodspa.org/2154/Elected-Officials']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		bio = response.xpath('//div[@id="div11dfe0c8-eed1-4a15-9277-39ff4386d193"]/div/div/p[2]/text()').get()
		email = bio.split(" ")[8].strip(".")
		addr = " ".join(bio.split(" ")[16:23])[:-1]
		for quote in response.xpath("//tbody/tr"):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR" if quote.xpath("td[2]//text()").get()=="Mayor" else "MEMBER OF COUNCIL",
				name=quote.xpath("td[1]//text()").get(),
				email=email,
				address=addr,
				url=response.url)
