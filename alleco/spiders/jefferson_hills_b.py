import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class jefferson_hills_b(scrapy.Spider):
	name = "jefferson_hills_b" # name of spider
	muniName = "JEFFERSON HILLS" # name of municipality
	muniType = "BOROUGH" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["https://www.jeffersonhillsboro.org/ElectedOfficials.aspx",
		'https://www.jeffersonhillsboro.org/Taxes.aspx'] # urls for requests go here
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
		if "Officials" in response.url:
			for quote in response.xpath("//span[@id='ContentPage1_ctl04_lblText']/table//tr"):
				allText = getAllText(quote)
				print(allText)
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR" if allText[0]=="Mayor" else "MEMBER OF COUNCIL",
					name=allText[1]+" "+allText[2],
					#email has to be manual because the site has weird server-side protections
					email=(allText[1][0]+allText[2]+"@jeffersonhills.net").lower(),
					url=response.url)
		elif "Taxes" in response.url:
			for quote in response.xpath("//tr[td/text()='Real Estate Tax Collector\xa0']"):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath("td[2]/text()").get().split("(")[1].strip()[:-1],
					phone=quote.xpath("td[2]/text()").get(),
					url=response.url)
