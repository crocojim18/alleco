import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getTextOfType
from alleco.objects.official import getAllText

class munhall_b(scrapy.Spider):
	name = "munhall_b" # name of spider
	muniName = "MUNHALL" # name of municipality
	muniType = "BOROUGH" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["http://www.munhallpa.us/contact-munhall-borough/elected-officials/"] # urls for requests go here
		for url in urls:
			yield scrapy.Request(
				url=url,
				callback=self.parse,
				# headers is only necessary if the website has a robots.txt file
				# which normally blocks web scraping
				# the header tricks the site into thinking it is being accessed by a browser
				headers={'User-Agent':
					'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'}
				)

	def parse(self, response):
		for quote in response.xpath("//h1[contains(text(),'Elected Officials')]/../../div"):
			names = getTextOfType(quote,"h3")
			allText = getAllText(quote)
			allPeeps = allText[:-3]
			phone = allText[-1]
			split = []
			temp = []
			for i in allText:
				if i in names and temp!=[]:
					split.append(temp)
					temp = []
				temp.append(i)
			split.append(temp)
			print(split)
			for person in split:
				office = "TAX COLLECTOR" if "Tax" in person[1] else "MAYOR" if person[1]=="Mayor" else "MEMBER OF COUNCIL"
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office=office,
					name=person[0],
					phone=phone if office=="MEMBER OF COUNCIL" else None,
					url=response.url)
