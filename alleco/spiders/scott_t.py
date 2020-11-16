import scrapy
from alleco.objects.official import Official

class scott_t(scrapy.Spider):
	name = "scott_t"
	muniName = "SCOTT"
	muniType = "TOWNSHIP"
	complete = True

	def start_requests(self):
		urls = ['https://scott-twp.com/government/board-of-commissioners/','https://scott-twp.com/departments/taxes/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if "commissioners" in response.url:
			for quote in response.xpath('//div[@class="commissioners"]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="COMMISSIONER",
					phone=quote.xpath("p[contains(text(),'-')]/text()[1]").get(),
					name=quote.xpath("h1/text()").get().split(",")[0],
					district=quote.xpath("h2/text()").get().upper(),
					url=response.url)
		elif "taxes" in response.url:
			for quote in response.xpath('//div[@class="contact"]')[0:1]:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					phone=quote.xpath("p[1]/text()[3]").get(),
					address=", ".join(quote.xpath("p[1]/text()").getall()[0:2]),
					name=quote.xpath("h1/text()").get(),
					url=response.url)
