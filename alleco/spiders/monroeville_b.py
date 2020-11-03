import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText
from re import sub

class monroeville_b(scrapy.Spider):
	name = "monroeville_b"
	muniName = "MONROEVILLE"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['https://www.monroeville.pa.us/elected.htm']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		counter = 0
		for quote in response.xpath('//td[@width="609"]/table'):
			names = [sub(r"\s+"," ",i) for i in getAllText(quote)]
			if counter==0: names = names[1:5]
			emails = [i for i in quote.xpath('.//a/@href').getall() if "mailto:" in i]
			counter += 1
			for x in range(len(names)//4):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL" if "Council" in names[x*4+1] else names[x*4+1].upper(),
					name=names[x*4],
					email=emails[x],
					district="AT-LARGE" if "Ward" not in names[x*4+1] else names[x*4+1][:6].upper(),
					phone=names[x*4+2],
					url=response.url)
