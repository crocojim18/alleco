import scrapy
from alleco.objects.official import Official

class braddock_b(scrapy.Spider):
	name = "braddock_b"
	muniName = "BRADDOCK"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['http://www.braddockborough.com/council/',
				'http://www.braddockborough.com/staff',
				'https://www.braddockborough.com/council/chardae-jones']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-1] == "s":
			for quote in response.xpath("//div[contains(@class, 'row container-box-med') and contains(.//div/@class, 'it-grid-one start bl')]"):
				bio = quote.xpath('div/p/text()').getall()
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=" ".join(quote.xpath("div/h1/text()").get().split(" ")[1:3]),
					phone=bio[-1],
					email=bio[-3].replace(" ",""),
					url=response.url)
		elif response.url[-1] == "/":
			for quote in response.xpath("//div[@class='med information-text']//div[@class='itg-teambox']")[1:]:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=quote.xpath("h3/text()").get(),
					district=self._districts(quote.xpath("h3/text()").get()),
					url=response.url)
		elif response.url[-1] == "f":
			for quote in response.xpath("//p[contains(text(), 'Tax Department Manager')]/.."):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath("h3/text()").get(),
					url=response.url)

	def _districts(self, string):
		#Note: In the future, figure out a better way to do this
		#Because this information is not on the Braddock website,
		#I am using the 2017 and 2019 election records to deduce districts

		if string=="Rob Parker": return "WARD 3"
		elif string=="Lorne Berry": return "WARD 2"
		elif string=="Tina Doose": return "WARD 2"
		elif string=="De Andrea Dudley": return "WARD 1"
		elif string=="Charlotte Clark": return "WARD 3"
		elif string=="Kevin Henderson": return "WARD 1"
		else: return None