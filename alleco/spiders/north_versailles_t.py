import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class north_versailles_t(scrapy.Spider):
	name = "north_versailles_t" # name of spider
	muniName = "NORTH VERSAILLES" # name of municipality
	muniType = "TOWNSHIP" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["https://nvtpa.com/elected-officials/",
		"https://nvtpa.com/tax-collector/"] # urls for requests go here
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
			for quote in response.xpath("//div[contains(h4/strong/u/text(),'Ward ')]"):
				alltext = getAllText(quote)
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="COMMISSIONER",
					name=alltext[2],
					district=alltext[0].upper(),
					termEnd=alltext[1],
					address=alltext[3]+", "+alltext[4],
					phone=alltext[5],
					url=response.url)
		elif "tax" in response.url:
			name = response.xpath("//h3[contains(u/text(),'-Tax Collector')]/u/text()").get().split("-")[0]
			address = getAllText(response.xpath("//div[contains(strong/text(),'Tax Office')]"))[1]
			phone = getAllText(response.xpath("//div[strong/text()='Phone:']"))
			print(phone)
			phone = phone[1]
			email = getAllText(response.xpath("//div[contains(strong/text(),'Email:')]"))[1]
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=name,
				address=address,
				phone=phone,
				email=email,
				url=response.url)