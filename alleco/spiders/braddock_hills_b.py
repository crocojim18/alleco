import scrapy
from alleco.objects.official import Official
from string import capwords

class braddock_hills_b(scrapy.Spider):
	name = "braddock_hills_b"
	muniName = "BRADDOCK HILLS"
	muniType = "BOROUGH"

	def start_requests(self):
		urls = ['https://www.braddockhillspa.com/what-we-do.html',
				'https://www.braddockhillspa.com/taxes.html']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-6] == "s":
			for quote in response.xpath("//div[@id='wsb-element-00000000-0000-0000-0000-000616789751']/div/p[2]"):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=" ".join(quote.xpath("font/span/text()").get().split(" ")[6:]).strip().strip("."),
					url=response.url)
		elif response.url[-6] == "o":
			ids=['wsb-element-6b355e90-6b08-4c88-8631-e1728857eb45',
				'wsb-element-00000000-0000-0000-0000-000616778570',
				'wsb-element-9b91db7a-8a0c-4f9d-a52f-79dd817d0906',
				'wsb-element-00000000-0000-0000-0000-000616876911',
				'wsb-element-00000000-0000-0000-0000-000616878242',
				'wsb-element-46955a32-8789-444c-91a0-1c24ca7c67f9',
				'wsb-element-00000000-0000-0000-0000-000616877933']
			for bit in ids:
				for quote in response.xpath("//div[@id='{}']".format(bit)):
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="MEMBER OF COUNCIL",
						name=quote.xpath(".//b/text()").get(),
						termStart=self._start(quote.xpath(".//span[contains(text(), 'elected') or contains(text(), 'appointed')]/text()").getall()),
						url=response.url)
			for quote in response.xpath("//div[@id='wsb-element-00000000-0000-0000-0000-000616778561']"):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=self._mayorName(response),
					termStart=self._start(quote.xpath(".//span[contains(text(), 'Elected')]/text()").getall()),
					url=response.url)

	def _start(self, strings):
		if len(strings)==0: return None
		return strings[-1].split(":")[-1].strip()

	def _mayorName(self, response):
		toRet = response.xpath("//div[@id='wsb-element-00000000-0000-0000-0000-000616778551']//h1/text()").get()
		toRet = " ".join(toRet.split(" ")[1:])
		return capwords(toRet)