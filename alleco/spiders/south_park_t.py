import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class south_park_t(scrapy.Spider):
	name = "south_park_t" # name of spider
	muniName = "SOUTH PARK" # name of municipality
	muniType = "TOWNSHIP" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["http://www.southparktwp.com/officials_elected.php"] # urls for requests go here
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
		supervisors = getAllText(response.xpath("//table[@id='Table1']"))
		for i in range(len(supervisors)//2):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="SUPERVISOR",
				name=supervisors[i].split(",")[0],
				phone=supervisors[i+3],
				url=response.url)
		for quote in response.xpath("//b[contains(text(),'Real Estate Tax Collector')]/.."):
			taxman = quote.xpath("./u/strong/text()").get().strip()
			taxinfo = [i.strip() for i in quote.xpath("./text()").getall() if len(i.strip())!=0][2].split(" ")
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=taxman,
				address=" ".join(taxinfo[10:19])[:-1],
				phone=taxinfo[-7],
				url=response.url)
		auditors = getAllText(response.xpath("//font[contains(b/text(),'Board of Auditors')]"))
		audArr = [auditors[3],auditors[5][:-1],auditors[7]]
		for person in audArr:
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="AUDITOR",
				name=person,
				url=response.url)
