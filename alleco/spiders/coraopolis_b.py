import scrapy
from alleco.objects.official import Official

class coraopolis_b(scrapy.Spider):
	name = "coraopolis_b"
	muniName = "CORAOPOLIS"
	muniType = "BOROUGH"
	complete = False

	def start_requests(self):
		urls = ['http://coraopolispa.com/council-and-borough-meetings/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//div[@class="entry-summary"]/p[7]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				name=quote.xpath("text()[1]").get().split("–")[0],
				address=self._address(quote.xpath("text()[2]").get().strip()),
				phone=quote.xpath("text()[3]").get().split("(")[0],
				email=quote.xpath("text()[3]").get().split(")")[1].strip(),				
				url=response.url)
		for quote in response.xpath('//div[@class="entry-summary"]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MEMBER OF COUNCIL",
				name=quote.xpath("p[15]/text()").get(),
				address=self._address(quote.xpath("p[16]/text()").get().strip()),
				phone=quote.xpath("p[17]/text()").get().split("(")[0],
				district="WARD 1",
				url=response.url)
		nodesToCheck = [9,10,11,12,13,14,18]
		for x in nodesToCheck:
			for quote in response.xpath('//div[@class="entry-summary"]/p[{}]'.format(x)):
				thisName = quote.xpath("text()[1]").get().split("–")[0]
				lastName = thisName.strip().split(" ")[-1]
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=thisName,
					address=self._address(quote.xpath("text()[2]").get().strip()),
					phone=None if quote.xpath("text()[3]").get() ==None else quote.xpath("text()[3]").get().split("(")[0],
					district=self._wards(lastName),
					url=response.url)
		#### ADDITIONAL EXPECTED ELECTED POSITIONS:
		#### TAX COLLECTOR
		#### UNABLE TO BE FOUND ON THEIR WEBSITE

	def _address(self, string):
		city = ", Coraopolis, PA 15108"
		return string+city

	# This information is not on the website
	# Ward divisions come from the 2017 and 2019 municipal election records
	def _wards(self, string):
		if string=="Cardimen": return "WARD 4"
		elif string=="Wade": return "WARD 3"
		elif string=="Bolea": return "WARD 2"
		elif string=="Kraynyk": return "WARD 3"
		elif string=="Pendel": return "WARD 2"
		elif string=="LaRocco": return "WARD 4"
		elif string=="Pitassi": return "WARD 1"
		elif string=="Mihalyi": return "WARD 1"
		else: None
