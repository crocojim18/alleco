import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class harrison_t(scrapy.Spider):
	name = "harrison_t" # name of spider
	muniName = "HARRISON" # name of municipality
	muniType = "TOWNSHIP" # type of municipality - township, borough, etc.
	complete = True # do not change until spider is complete

	def start_requests(self):
		urls = ["http://harrisontwp.com/board-agendas-and-minutes/",
		'http://harrisontwp.com/taxes/'] # urls for requests go here
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
		if "board" in response.url:
			for quote in response.xpath("//h2[contains(text(),'Board Members')]/.."):
				alltext = [i for i in getAllText(quote)[1:] if i!=',' and "Chairman" not in i]
				for i in range(len(alltext)//5):
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="COMMISSIONER",
						name=alltext[i*5],
						district="WARD "+alltext[i*5+2],
						email=alltext[i*5+1] if "@" in alltext[i*5+1] else None,
						phone=alltext[i*5+1] if "(" in alltext[i*5+1] else None,
						termEnd=alltext[i*5+4][-4:],
						url=response.url)
		elif 'taxes' in response.url:
			quote = response.xpath("//p[contains(strong/text(),'Delinquent Earned Income Tax Collector:')]/following-sibling::p/text()").getall()[0:4]
			quote = [i.replace("\xa0","").strip() for i in quote]
			print(quote)
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=quote[0],
				phone=quote[1],
				address=quote[2]+", "+quote[3],
				url=response.url)
