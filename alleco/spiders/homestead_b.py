import scrapy, re
from alleco.objects.official import Official

class homestead_b(scrapy.Spider):
	name = "homestead_b" # name of spider
	muniName = "HOMESTEAD" # name of municipality
	muniType = "BOROUGH" # type of municipality - township, borough, etc.
	complete = False # do not change until spider is complete

	def start_requests(self):
		urls = ["http://www.homesteadborough.com/government/mayor_council/default.aspx"] # urls for requests go here
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
		# The website is inaccurate because they have one person listed as a member twice
		for quote in response.xpath("//h3[contains(text(),'Our Mayor')]/following-sibling::p")[0:1]:
			print(quote)
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				name=quote.xpath("./text()").get().split(",")[0],
				url=response.url)
		for quote in response.xpath("//h3[contains(text(),'Council Members')]/following-sibling::ul/li"):
			name=quote.xpath(".//text()").get().split(",")[0].strip()
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MEMBER OF COUNCIL",
				district=self._district(name),
				name=name,
				url=response.url)
		## Incomplete: expected 1 tax collector, unable to be found on website

	#Because the information on the site disagrees with the election record and is likely out of date,
	#There is missing information here
	def _district(self, string):
		bits = {"Don Dais":"UNKNOWN",
		"Drew Borcik":"WARD 3",
		"Donald Dais":"UNKNOWN",
		"Jou-Al Burwell":"UNKNOWN",
		"Mary Nesby":"WARD 2",
		"Minister Connie Burwell":"WARD 2",
		"Lloyd Cunningham":"WARD 1"}
		return None if string not in bits else bits[string]
