import scrapy
from alleco.objects.official import Official

class collier_t(scrapy.Spider):
	name = "collier_t"
	muniName = "COLLIER"
	muniType = "TOWNSHIP"
	complete = True

	def start_requests(self):
		urls = ['https://www.colliertownship.net/242/Collier-Township-Officials']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		counter = 0
		for quote in response.xpath('//div[@class="fr-view"]/ul'):
			if counter == 0:
				for person in quote.xpath("li"):
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="COMMISSIONER",
						name=self._name(person.xpath("text()").get()),
						url=response.url)
			elif counter == 1:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=self._name(quote.xpath("li/text()").get()),
					url=response.url)
			counter += 1

	def _name(self, string):
		return string.split(" - ")[0].split(",")[0]
