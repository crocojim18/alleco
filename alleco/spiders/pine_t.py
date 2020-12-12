import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText
from alleco.objects.official import getAllLinks

class pine_t(scrapy.Spider):
	name = "pine_t" # name of spider
	muniName = "PINE" # name of municipality
	muniType = "TOWNSHIP" # type of municipality - township, borough, etc.
	complete = True

	def start_requests(self):
		urls = ["https://twp.pine.pa.us/191/Board-of-Supervisors"] # urls for requests go here
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		surnames = {}
		sidearr = []
		sidelinks = getAllLinks(response.xpath("//h4[contains(text(),'Board of Supervisors')]/../.."))
		for parts in response.xpath("//h4[contains(text(),'Board of Supervisors')]/../../li"):
			sidearr.append(getAllText(parts))
		index = 0
		for person in sidearr[1:]:
			surnames[person[0].split(" ")[-1]] = sidelinks[index]
			index += 1
		addr = sidearr[0][2]+", "+"".join(sidearr[0][3:5])+" "+sidearr[0][5]+" "+sidearr[0][6]
		phone = sidearr[0][7]
		for quote in response.xpath("//h2[contains(text(),'Members')]/../../../../../..//li"):
			bits = getAllText(quote)
			name = bits[0].split(",")[0]
			termEnd = bits[1]
			email = surnames[name.split(" ")[-1]]
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="SUPERVISOR",
				name=name,
				termEnd=termEnd,
				email=email,
				address=addr,
				phone=phone,
				url=response.url)
