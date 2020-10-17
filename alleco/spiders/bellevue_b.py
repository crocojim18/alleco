import scrapy
from alleco.objects.official import Official

class bellevue_b(scrapy.Spider):
	name = "bellevue_b"
	muniName = "BELLEVUE"
	muniType = "BOROUGH"

	def start_requests(self):
		urls = ['https://www.bellevuepa.org/government']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		wards = [[10,11,12],[15,16,17],[20,21,22]]
		self.address = self._address(response.xpath('//div[@id="comp-j45vf6qp"]/p[2]//text()').getall()[1:])
		self.phone = self._phone(response.xpath('//div[@id="comp-j45vf6qp"]/p[3]//text()').get())
		for quote in response.xpath('//div[@id="comp-j45vf6qp"]/h6[5]/span'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				name=quote.xpath("./text()").get(),
				email=quote.xpath(".//a/@href").get(),
				url=response.url,
				address=self.address,
				phone=self.phone)
		counter = 1
		for ward in wards:
			for place in ward:
				for quote in response.xpath('//div[@id="comp-j45vf6qp"]/h6[{}]'.format(place)):
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="MEMBER OF COUNCIL",
						district="WARD {}".format(counter),
						email=quote.xpath(".//a/@href").get(),
						name=quote.xpath("span/text()").get(),
						url=response.url,
						address=self.address,
						phone=self.phone)
			counter += 1
		for quote in response.xpath('//div[@id="comp-j45vf6qp"]/h6[25]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				email=quote.xpath(".//a/@href").get(),
				name=quote.xpath("span/text()").get(),
				url=response.url,
				address=self.address,
				phone=self.phone)
		for quote in response.xpath('//div[@id="comp-j45vf6qp"]/h6')[27:30]:
			if quote.xpath("span/text()").get().strip()!="\u200b":
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="AUDITOR",
					name=quote.xpath("span/text()").get(),
					url=response.url,
					address=self.address,
					phone=self.phone)
			else:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="AUDITOR",
					name=None,
					url=response.url,
					vacant=True)

	def _address(self, lines):
		return ", ".join([x.strip() for x in lines])

	def _phone(self, string):
		return string.split(" ")[7]