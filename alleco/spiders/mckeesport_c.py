import scrapy
from re import search
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class mckeesport_c(scrapy.Spider):
	name = "mckeesport_c" # name of spider
	muniName = "MCKEESPORT" # name of municipality
	muniType = "CITY" # type of municipality - township, borough, etc.
	complete = False # do not change until spider is complete

	def start_requests(self):
		urls = ["https://www.mckeesport-pa.gov/Directory.aspx?did=17",
		'https://www.mckeesport-pa.gov/Directory.aspx?did=19'] # urls for requests go here
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
		if response.url[-1]=="7":
			universals = response.xpath("//span[@class='DirectoryNormalText' and contains(label/text(),'Physical Address')]")
			allText = getAllText(universals)
			address = ", ".join(allText[1:4])
			for quote in response.xpath("//tr[td/span/text()='Mayor']"):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					address=address,
					office="MAYOR",
					email=self._email(quote.xpath('td[3]/span/script/text()').get()),
					phone=quote.xpath('td[4]/span/text()').get(),
					name=self._name(quote.xpath('td[1]/span/a/text()').get()),
					url=response.url)
		elif response.url[-1]=="9":
			universals = response.xpath("//span[@class='DirectoryNormalText' and contains(label/text(),'Physical Address')]")
			allText = getAllText(universals)
			address = ", ".join(allText[5:8])
			phone = allText[-2]
			for quote in response.xpath("//table[@id='cityDirectoryDepartmentDetails']//tr[contains(td[2]/span/text(), 'Council')]"):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					address=address,
					office="MEMBER OF COUNCIL",
					phone=phone,
					name=self._name(quote.xpath('td[1]/span/a/text()').get()),
					url=response.url)
		## EXPECTED: 1 CONTROLLER AT-LARGE

	def _email(self,string):
		if string==None: return None
		first = search(r"var w = '(.*?)';",string)
		second = search(r"var x = '(.*?)';",string)
		if second != None and first != None:
			return first[1]+"@"+second[1]
		else: return None

	def _name(self,string):
		string = string.split(", ")
		string.reverse()
		return " ".join(string)