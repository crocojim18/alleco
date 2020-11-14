import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class duquesne_c(scrapy.Spider):
	name = "duquesne_c"
	muniName = "DUQUESNE"
	muniType = "CITY"
	complete = False

	def start_requests(self):
		urls = ['http://duquesnepa.us/elected_officials', 'http://duquesnepa.us/city_officials']
		for url in urls:
			yield scrapy.Request(url=url, 
				callback=self.parse, 
				headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
				})

	def parse(self, response):
		if "elected" in response.url:
			folks = []
			bits = getAllText(response.xpath('//td[@id="esbCr2x1"]/..'))
			temp = []
			for i in bits:
				if "Mayor" in i or "City Council" in i:
					if len(temp)>0: folks.append(temp)
					temp = [i]
				else:
					temp.append(i)
			folks.append(temp)
			for folk in folks:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL" if folk[0]=="City Council" else "MAYOR",
					name=folk[1],
					email=None if len(folk)<3 else folk[2],
					url=response.url)
		elif "city" in response.url:
			bits = getAllText(response.xpath('//span[contains(text(),"Treasurer")]/../../..'))
			print(bits)
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TREASURER",
				name=bits[1],
				url=response.url)
		#EXPECTED: 1 at-large controller
		#Unable to be found on the Duquesne website