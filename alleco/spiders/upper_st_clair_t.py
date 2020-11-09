import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class upper_st_clair_t(scrapy.Spider):
	name = "upper_st_clair_t"
	muniName = "UPPER ST. CLAIR"
	muniType = "TOWNSHIP"
	complete = True

	def start_requests(self):
		urls = ['http://www.twpusc.org/government/elected-officials']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath("//tr[contains(td/text(),'Commissioner')]/../tr")[1:]:
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="COMMISSIONER",
				name=quote.xpath("td[1]/text()").get().split(',')[0],
				district="AT-LARGE" if quote.xpath("td[2]/text()").get().strip()=="At Large" else quote.xpath("td[2]/text()").get().upper(),
				termEnd=quote.xpath("td[4]/text()").get(),
				url=response.url)
