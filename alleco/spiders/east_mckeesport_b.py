import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class east_mckeesport_b(scrapy.Spider):
	name = "east_mckeesport_b"
	muniName = "EAST MCKEESPORT"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['http://eastmckeesportboro.com/contactus.htm',
		'http://eastmckeesportboro.com/taxcollector.htm']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if "taxcollector" in response.url:
			addr = getAllText(response.xpath("//p[text()[contains(.,'Tax Office Address')]]"))[-2:]
			addr[1] = " ".join([i.upper() if i=="Pa" else i+"," if i=="McKeesport" else i for i in addr[1].split(" ")])
			email = response.xpath("//p[text()[contains(.,'E-mail')]]/a/@href").get()
			phone = response.xpath("//p[contains(text(),'Phone')]/text()").get()
			for quote in response.xpath('//p[contains(text(), "Tax Collector")]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath("./text()").get().split("-")[0],
					address=", ".join(addr),
					email=email,
					phone=phone,
					url=response.url)
		elif "contact" in response.url:
			parts = getAllText(response.xpath('//p[contains(text(), "Council")]'))[:-2]
			for i in range(len(parts)//2):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=parts[i*2].split(":")[1].split("-")[0],
					email=parts[i*2+1],
					url=response.url)
			for quote in response.xpath('//p[contains(text(), "Mayor")]'):
				email = {"email": quote.xpath("a/@href").get().split(":")[1]}
				url = "http://eastmckeesportboro.com/leaders.htm"
				req = scrapy.Request(url=url, callback=self.mayorParse, cb_kwargs=email)
				yield req

	def mayorParse(self, response, email):
		yield Official(
			muniName=self.muniName,
			muniType=self.muniType,
			office="MAYOR",
			name=response.xpath("//p[contains(text(),'Mayor')]/text()").get().split(":")[1],
			email=email,
			url=response.url)