import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText
from re import search

class north_fayette_t(scrapy.Spider):
	name = "north_fayette_t"
	muniName = "NORTH FAYETTE"
	muniType = "TOWNSHIP"
	complete = False

	def start_requests(self):
		urls = ['https://north-fayette.com/Directory.aspx?did=7',
		'https://north-fayette.com/Directory.aspx?DID=12']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-1]=="7":
			for quote in response.xpath('//tr/td[contains(span/text(),"Tax Coll")]/..'):
				name = quote.xpath("td[1]/span/a/text()").get().split(", ")
				name.reverse()
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=" ".join(name),
					phone=quote.xpath("td[4]/span/text()").get(),
					email=self._email(quote.xpath(".//script").get()),
					address=", ".join([i.strip() for i in quote.xpath("//span[@class='DirectoryNormalText'][1]/p[1]/text()").getall()]),
					url=response.url)
		elif response.url[-1]=='2':
			for quote in response.xpath('//table/tr'):
				phone = quote.xpath("td[4]/span/text()").get().strip()
				name = quote.xpath("td[1]/span/a/text()").get().split(", ")
				name.reverse()
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="SUPERVISOR",
					name=" ".join(name),
					phone=None if phone=='' else phone,
					email=self._email(quote.xpath(".//script").get()),
					address=", ".join([i.strip() for i in quote.xpath("//span[@class='DirectoryNormalText'][1]/p[1]/text()").getall()]),
					url=response.url)
		##EXPECTED: 3 AUDITORS

	def _email(self,script):
		bits = search(r"var w = '(.+?)';\s+var x = '(.+?)'", script)#
		if not bits: return None
		else:
			return bits[1]+"@"+bits[2]