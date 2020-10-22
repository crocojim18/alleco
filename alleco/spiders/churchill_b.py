import scrapy
from alleco.objects.official import Official

class churchill_b(scrapy.Spider):
	name = "churchill_b"
	muniName = "CHURCHILL"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['http://www.churchillborough.com/churchill-administration/officials-committees.aspx']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//table[contains(.//h3,"Mayor")]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				name=self._name(quote.xpath("tr[2]//strong/text()").get()),
				email=quote.xpath("tr[2]//a/@href").get(),
				termEnd=quote.xpath("tr[2]/td[2]/p/text()").get(),
				url=response.url)
		for quote in response.xpath('//table[contains(.//h3,"Churchill Borough Council")]/tr[contains(.//strong, "(")]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MEMBER OF COUNCIL",
				name=self._name(quote.xpath(".//strong/text()").get()),
				email=quote.xpath(".//a/@href").get(),
				termEnd=quote.xpath("./td[2]/p/text()").get(),
				url=response.url)
		for quote in response.xpath('//table[contains(.//h3,"Real Estate Tax Collector")]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				name=self._name(quote.xpath("tr[2]//strong/text()").get()),
				termEnd=quote.xpath("tr[2]/td[2]/p/text()").get(),
				url=response.url)
		
	def _name(self, string):
		return string.split(" (")[0]
