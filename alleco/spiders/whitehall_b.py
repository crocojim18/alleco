import scrapy, re
from alleco.objects.official import Official

class whitehall_b(scrapy.Spider):
	name = "whitehall_b" # name of spider
	muniName = "WHITEHALL" # name of municipality
	muniType = "BOROUGH" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["https://whitehallboro.org/government/officials/",
		'https://whitehallboro.org/for-residents/taxes/'] # urls for requests go here
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
		if "officials" in response.url:
			for quote in response.xpath("//p[contains(text(),'Council Member') or contains(text(),'Mayor')]/.."):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR" if "Mayor" in quote.xpath("p/text()").get() else "MEMBER OF COUNCIL",
					name=quote.xpath("h3/text()").get().split(",")[0],
					url=response.url)
		elif "taxes" in response.url:
			for quote in [response.xpath("//text()[contains(.,'Whitehall Borough Tax Collector')]").get()]:
				part = quote.split(", ")[-1].split(" ")
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=" ".join(part[0:2]),
					email=part[-1],
					phone=part[-3],
					url=response.url)
