import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText
from re import search

class hampton_t(scrapy.Spider):
	name = "hampton_t"
	muniName = "HAMPTON"
	muniType = "TOWNSHIP"
	complete = True

	def start_requests(self):
		urls = ['https://www.hampton-pa.org/162/Council']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//div[@id="divEditoreb0366d2-7125-4b47-bda5-1c51fbac2709"]'):
			bits = getAllText(quote)
			bits = bits[1].split(",")[0].strip(":")
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MEMBER OF COUNCIL",
				name=bits,
				url=response.url)
			for link in quote.xpath(".//a"):
				url = link.xpath("./@href").get()
				req = scrapy.Request(url=url, callback=self.linkParse)
				yield req

	def linkParse(self,response):
		for quote in response.xpath("//div[contains(a/text(),'Council')]"):
			yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL" if "Controller" not in quote.xpath('./text()[2]').get() else "CONTROLLER",
					name=quote.xpath('../h1/text()').get(),
					email=self._email(quote.xpath('./script/text()').get()),
					url=response.url)

	def _email(self,string):
		if string==None: return None
		first = search(r"var wsd='(.*?)';",string)
		second = search(r"var xsd='(.*?)';",string)
		if second != None and first != None:
			return first[1]+"@"+second[1]
		else: return None