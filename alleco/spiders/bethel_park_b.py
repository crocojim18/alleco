import scrapy
from alleco.objects.official import Official
from datetime import date

class bethel_park_b(scrapy.Spider):
	name = "bethel_park_b"
	muniName = "BETHEL PARK"
	muniType = "BOROUGH"

	def start_requests(self):
		urls = ['https://bethelpark.net/home-page/government/councilmayor/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		counter = 0
		for quote in response.xpath('//div[@class="fusion-text fusion-text-2"]/table/tbody/tr'):
			if counter == 0:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=" ".join(quote.xpath("td[2]/text()").get().split(" ")[1:]),
					phone=quote.xpath("td[2]/text()").getall()[1].strip(),
					email=quote.xpath("td[2]/text()").getall()[2],
					termEnd=self._termEnd(quote.xpath("td[2]/text()").getall()[3]),
					url=response.url)
			else:
				parts = [x.strip() for x in quote.xpath("td[2]/p//text()").getall() if len(x.strip())>0]
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					district="WARD {}".format(counter),
					name=parts[0],
					phone=parts[1],
					email=parts[2],
					termEnd=self._termEnd(parts[3]),
					url=response.url)
			counter += 1

	def _termEnd(self, string):
		parts = string.strip().split(" ")[1:]
		return " ".join(parts)
