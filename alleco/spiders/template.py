import scrapy, re
from alleco.objects.official import Official

class name_class(scrapy.Spider):
	name = "name_class" # name of spider
	muniName = "MUNICIPALITY" # name of municipality
	muniType = "CLASS" # type of municipality - township, borough, etc.
	complete = False # do not change until spider is complete

	def start_requests(self):
		urls = [""] # urls for requests go here
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
		for quote in response.xpath(""):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="NAME OF OFFICE",
				name="J. Doe",
				url=response.url)
