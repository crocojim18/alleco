import scrapy
from alleco.objects.official import Official

class brentwood_b(scrapy.Spider):
	name = "brentwood_b"
	muniName = "BRENTWOOD"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['https://www.brentwoodboro.com/borough-council.html',
		'https://www.brentwoodboro.com/borough-mayor.html',
		'https://www.brentwoodboro.com/tax-collection.html']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-6]=='n':
			for quote in response.xpath("//div[@itemprop='articleBody']/p[1]"):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=self._taxCollector(quote.xpath("text()").get(),"name"),
					phone=self._taxCollector(quote.xpath("text()").get(),"phone"),
					url=response.url)
		elif response.url[-6]=='r':
			for quote in response.xpath("//div[@class='custom-title']"):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=quote.xpath("div[1]/text()").get(),
					phone=quote.xpath("div[3]/text()").get(),
					url=response.url)
		elif response.url[-6]=='l':
			for quote in response.xpath("//div[@id='rt-sidebar-a']/div[1]/div/div[2]/ul/li"):
				url = response.urljoin(quote.xpath('a/@href').get())
				req = scrapy.Request(url=url, callback=self.councilParse)
				yield req

	def _taxCollector(self, string,searchFor):
		sentences = string.split(". ")
		if searchFor == "name":
			return " ".join(sentences[1].split(" ")[0:2]).strip(",")
		elif searchFor == "phone":
			return sentences[3].split(" ")[10]
		return None

	def councilParse(self, response):
		for quote in response.xpath("//div[@class='custom-title']"):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MEMBER OF COUNCIL",
				name=[x for x in quote.xpath(".//text()").getall() if len(x.strip())>0][0],
				phone=[x for x in quote.xpath(".//text()").getall() if len(x.strip())>0][2],
				termStart=" ".join(quote.xpath("//*[contains(text(),'Member of Council since')]/text()").get().split(" ")[-3:]),
				termEnd=" ".join(quote.xpath("//*[contains(text(),'Term expires:')]/text()").get().split(" ")[-3:]),
				url=response.url)