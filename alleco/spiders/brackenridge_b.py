import scrapy
from alleco.objects.official import Official

class brackenridge_b(scrapy.Spider):
	name = "brackenridge_b"
	muniName = "BRACKENRIDGE"
	muniType = "BOROUGH"

	def start_requests(self):
		urls = ['http://brackenridgeboro.com/officials/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//div[@class="fl-rich-text"]/p')[1:9]:
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office=self._position(quote.xpath("text()").get())[0],
				district=self._position(quote.xpath("text()").get())[1],
				name=quote.xpath("text()").get().split("-")[0],
				url=response.url)

	def _position(self, string):
		string = string.split("-")[1].strip()
		listo = string.split(" ")[0:2]
		office = "MEMBER OF COUNCIL" if listo[0] == "Councilman" else " ".join(listo).upper()
		district = "AT-LARGE"
		if office == "MEMBER OF COUNCIL":
			if listo[1]=="Second": district = "WARD 2"
			elif listo[1]=="First": district = "WARD 1"
			elif listo[1]=="Third": district = "WARD 3"
		return (office,district)