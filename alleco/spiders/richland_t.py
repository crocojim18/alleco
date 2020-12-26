import scrapy, re
from alleco.objects.official import Official

class richland_t(scrapy.Spider):
	name = "richland_t" # name of spider
	muniName = "RICHLAND" # name of municipality
	muniType = "TOWNSHIP" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["https://richland.pa.us/government-administration/officials-and-committees/"] # urls for requests go here
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
		for quote in response.xpath("//h2[contains(text(),'BOARD OF SUPERVISORS')]/../../../../tbody[1]/tr"):
			district = quote.xpath("td[2]/text()").get().strip()
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="SUPERVISOR",
				name=quote.xpath("td[1]/text()").get().split(',')[0],
				district="AT-LARGE" if district=="At Large" else "DISTRICT "+str(int(district[-1])//2),
				termEnd=quote.xpath("td[3]/text()").get(),
				url=response.url)
