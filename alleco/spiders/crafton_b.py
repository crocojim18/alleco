import scrapy
from alleco.objects.official import Official

class crafton_b(scrapy.Spider):
	name = "crafton_b"
	muniName = "CRAFTON"
	muniType = "BOROUGH"
	complete = False

	def start_requests(self):
		urls = ['https://www.craftonborough.com/council-members	']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//div[@id="block-5bd7d8e6104c7b8d713191d8"]/div/ul')[0:2]:
			for person in quote.xpath("li"):
				line = self._name(person.xpath("p/text()").get())
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=line[0],
					email=line[1],
					url=response.url)
		for quote in response.xpath('//div[@id="block-5bd7d8e6104c7b8d713191d8"]/div/ul[3]'):
			for person in quote.xpath("li"):
				line = self._name(person.xpath("p/text()").get())
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=line[0],
					email=line[1],
					url=response.url)
	#### Additional Expected positions: 1 tax collector at-large
	#### Unable to be found on their website

	def _name(self, string):
		string = string.split(":")[-1]
		return string.split(", ")