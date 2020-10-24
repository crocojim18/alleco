import scrapy
from alleco.objects.official import Official

class crescent_t(scrapy.Spider):
	name = "crescent_t"
	muniName = "CRESCENT"
	muniType = "TOWNSHIP"
	complete = True
	wardDict = {}

	def start_requests(self):
		urls = ['http://crescenttownship.com/government/board-of-commissioners/',
		'http://crescenttownship.com/residents/utilities-taxes/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-3] == 'r':
			lines = []
			wardtemp = []
			for quote in response.xpath('//div[@class="panel-body"]')[0].xpath("p[5]/strong"):
				wardtemp.append(quote.xpath("text()").get().strip("-").split("Commissioner ")[-1])
			self.wardDict = {wardtemp[1]:wardtemp[0], wardtemp[3]:wardtemp[2]}
			print(self.wardDict)
			for quote in response.xpath('//div[@class="panel-body"]')[2].xpath("p")[0:4]:
				curr = [x.strip() for x in quote.xpath(".//text()").getall() if len(x.strip())>0]
				if len(curr)>4:
					lines.append(curr[0:3])
					lines.append(curr[3:])
				else: lines.append(curr)
			for line in lines:
				line = line[1:]
				newLine = []
				for token in line:
					newLine += [x for x in token.split("-") if len(x)>0]
				line = newLine
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="COMMISSIONER",
					name=line[0],
					termEnd=line[1].strip().split(" ")[-1],
					email=line[2],
					district=self._district(line[0]),
					url=response.url)
		elif response.url[-3] == 'e':
			for quote in response.xpath('//div[contains(h3/text(),"Crescent Township Tax Collector")]'):
				parts = [x.strip() for x in quote.xpath("text()").getall() if len(x.strip())>0]
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=parts[0],
					address=", ".join(parts[1:3]),
					phone=parts[3],
					email=parts[5].split(" ")[-1],
					url=response.url)

	def _district(self, string):
		return "AT-LARGE" if string.strip() not in self.wardDict else self.wardDict[string.strip()]
