import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class west_deer_t(scrapy.Spider):
	name = "west_deer_t" # name of spider
	muniName = "WEST DEER" # name of municipality
	muniType = "TOWNSHIP" # type of municipality - township, borough, etc.
	complete = False # do not change until spider is complete

	def start_requests(self):
		urls = ["http://www.westdeertownship.com/board-of-supervisors/",
		"http://www.westdeertownship.com/tax-collection/"] # urls for requests go here
		for url in urls:
			yield scrapy.Request(url=url,callback=self.parse)

	def parse(self, response):
		if "supervisors" in response.url:
			for quote in response.xpath("//div[contains(h2/text(),'Current Board of Supervisors')]/ul/li"):
				name = quote.xpath("text()").get().split("–")[0]
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="SUPERVISOR",
					name=name,
					district=self._district(name),
					url=response.url)
		elif "tax" in response.url:
			for quote in response.xpath("//div[@class='entry']"):
				name = getAllText(quote.xpath('p[13]'))
				email = quote.xpath('p[14]/a/@href').get()
				tempAddr = name[3].split(" ")
				addr = " ".join([tempAddr[0],"PA",tempAddr[2]])
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=name[0],
					address=name[2]+", "+addr,
					phone=name[4].replace(".",""),
					email=email,
					url=response.url)
		## EXPECTED
		## 3 AUDITORS ELECTED AT-LARGE
		## UNABLE TO BE FOUND ON WEBSITE

	#This information is not on the website and is taken from the Home Rule Charter and the 2019 Election Returns
	def _district(self, string):
		if "Forbes" in string:
			return "DISTRICT 1"
		elif "Hollibaugh" in string:
			return "DISTRICT 3"
		else:
			return "AT-LARGE"