import scrapy, re
from alleco.objects.official import Official

class white_oak_b(scrapy.Spider):
	name = "white_oak_b" # name of spider
	muniName = "WHITE OAK" # name of municipality
	muniType = "BOROUGH" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["http://www.woboro.com/contacts-072607.htm"] # urls for requests go here
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
		for quote in response.xpath("//tr[contains(td/text(),'Mayor - Council - Borough Manager')]/../tr")[2:-1]:
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR" if "Mayor" in quote.xpath("td[1]/text()").get() else "MEMBER OF COUNCIL",
				name=quote.xpath("td[2]/text()").get(),
				url=response.url)
		for quote in response.xpath("//tr[contains(td/text(),'Property Tax Collector - ')]"):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=quote.xpath("td[1]/text()").get().split(" - ")[-1],
				phone=quote.xpath("td[2]/text()").get(),
				url=response.url)
