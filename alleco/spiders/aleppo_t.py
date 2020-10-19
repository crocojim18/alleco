import scrapy
from alleco.objects.official import Official
from datetime import date

class aleppo_t(scrapy.Spider):
	name = "aleppo_t"
	muniName = "ALEPPO"
	muniType = "TOWNSHIP"

	def start_requests(self):
		urls = ['https://aleppotownship.com/officials/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//div[@class="et_pb_text_inner"]/div[@style="text-align: center;"]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="COMMISSIONER",
				name=quote.xpath("div/text()").get().strip().strip(","),
				email=quote.xpath("div/a/text()").get(),
				url=response.url,
				termEnd=self._termEnd(quote.xpath("div[3]/text()").get()))
		for quote in response.xpath('//p[contains(strong/text(),"Tax Collector")]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=quote.xpath("text()").get(),
				url=response.url)

	def _termEnd(self, string):
		parts = string.strip().split(" ")[2:]
		return " ".join(parts)