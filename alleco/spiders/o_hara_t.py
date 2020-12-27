import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class o_hara_t(scrapy.Spider):
	name = "o_hara_t" # name of spider
	muniName = "O'HARA" # name of municipality
	muniType = "TOWNSHIP" # type of municipality - township, borough, etc.
	complete = False # do not change until spider is complete

	def start_requests(self):
		urls = ["https://www.ohara.pa.us/township-council"] # urls for requests go here
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
		for quote in response.xpath("//th[contains(text(),'Name')]/../../../tbody/tr"):
			allText = getAllText(quote)
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TREASURER" if "Treasurer" in allText[1] else "MEMBER OF COUNCIL",
				district=self._district(allText[1]),
				name=allText[0],
				phone=None if len(allText)<3 else allText[2],
				url=response.url)
			## Expected: 3 AUDITORS AT-LARGE

	def _district(self,string):
		if "At-Large" in string or "Treasurer" in string:
			return "AT-LARGE"
		nums = ["First","Second","Third","Fourth","Fifth"]
		index = 1
		for i in nums:
			if i in string: return "WARD " + str(index)
			index+=1