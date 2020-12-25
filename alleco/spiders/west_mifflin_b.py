import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class west_mifflin_b(scrapy.Spider):
	name = "west_mifflin_b" # name of spider
	muniName = "WEST MIFFLIN" # name of municipality
	muniType = "BOROUGH" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["https://westmifflinborough.com/elected-officials/",
		'https://westmifflinborough.com/real-estate-taxes/'] # urls for requests go here
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if "elected" in response.url:
			for quote in response.xpath("//div[@class='et_pb_blurb_container']"):
				allText = getAllText(quote)
				email = quote.xpath(".//img/@alt").getall()
				if len(email)>0: email[0] = email[0].replace("mifflon", "mifflin")
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR" if allText[0]=="Mayor" else "MEMBER OF COUNCIL",
					name=allText[-1],
					email=None if email==[] else email[0],
					url=response.url)
		elif "taxes" in response.url:
			for quote in response.xpath("//div[@class='et_pb_text_inner']")[0:1]:
				allText = getAllText(quote)
				print(allText)
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					phone=allText[3],
					name=allText[0].split(',')[0],
					address=allText[1]+" "+allText[2],
					url=response.url)
