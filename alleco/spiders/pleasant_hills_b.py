import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class pleasant_hills_b(scrapy.Spider):
	name = "pleasant_hills_b" # name of spider
	muniName = "PLEASANT HILLS" # name of municipality
	muniType = "BOROUGH" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["https://www.pleasanthillspa.com/index.php/about-us/contact-us",
		"https://www.pleasanthillspa.com/index.php/services/taxes"] # urls for requests go here
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
		if "contact" in response.url:
			for quote in response.xpath("//form[@id='adminForm']/ul/li"):
				alltext = getAllText(quote)
				if "Council" in alltext[1] or "President" in alltext[1] or "Mayor" in alltext[1]:
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="MAYOR" if "Mayor"==alltext[1] else "MEMBER OF COUNCIL",
						name=alltext[0],
						url=response.url)
		elif "taxes" in response.url:
			for quote in response.xpath("//span[contains(strong/text(),'Mercantile Tax Collector')]"):
				alltext = getAllText(quote)
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=alltext[1].split(",")[0],
					address=", ".join([i.strip() for i in alltext[1].split(",")[1:-1]]),
					phone=alltext[2],
					url=response.url)