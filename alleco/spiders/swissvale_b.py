import scrapy, re
from alleco.objects.official import Official, getAllText

class name_class(scrapy.Spider):
	name = "swissvale_b"
	muniName = "SWISSVALE"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ["http://www.swissvaleborough.com/government/elected%20-officials.aspx"] # urls for requests go here
		for url in urls:
			yield scrapy.Request(
				url=url,
				callback=self.parse,
				headers={'User-Agent':
					'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}
				)

	def parse(self, response):
		for quote in response.xpath("//div[@class='twocolbig']"):
			alltext = getAllText(quote)
			# don't try to make the next line interact w quote it wouldn't work
			headers = getAllText(response.xpath("//div[@class='twocolbig']/h4"))
			for h in headers:
				loc = [e for e, part in enumerate(alltext) if h==alltext[e]][0]
				if "mayor" in h.lower():
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="MAYOR",
						name=alltext[loc+1],
						url=response.url)
				if h == "MEMBERS OF COUNCIL":
					for member in alltext[loc+1:loc+8]:
						yield Official(
							muniName=self.muniName,
							muniType=self.muniType,
							office="MEMBER OF COUNCIL",
							# if their position, e.g. pres or VP follows
							name=member.split(",")[0],
							url=response.url)
				if "tax" in h.lower():
						yield Official(
							muniName=self.muniName,
							muniType=self.muniType,
							office="TAX COLLECTOR",
							phone=alltext[loc+3].split(":")[1],
							name=alltext[loc+2],
							url=response.url)
