import scrapy, re
from alleco.objects.official import Official

class mccandless_t(scrapy.Spider):
	name = "mccandless_t"
	muniName = "MCCANDLESS"
	muniType = "TOWNSHIP"
	complete = True

	def start_requests(self):
		urls = ['https://www.townofmccandless.org/town-council']
		for url in urls:
			yield scrapy.Request(url=url, 
				callback=self.parse, 
				headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
				})

	def parse(self, response):
		for quote in response.xpath('//section[@class="field field-name-field-description field-type-text-with-summary field-label-hidden"]/table'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MEMBER OF COUNCIL",
				district=quote.xpath('thead/tr/th[2]/text()').get().split(",")[-1].strip().upper(),
				name=quote.xpath('thead/tr/th[1]/text()').get(),
				phone=quote.xpath('tr/td[2]/p[5]/text()').get(),
				termEnd=self._termEnd(quote.xpath('tr/td[2]/p[7]/text()').get()),
				email=quote.xpath('tr//a/@href').get(),
				address=", ".join([i.strip() for i in quote.xpath('tr/td[2]/p[1]/text()').getall()]),
				url=response.url)

	def _termEnd(self, string):
		parts = string.replace("\xa0",' ').strip().split(" ")[-3:]
		print(parts)
		if parts[0]=="1st" and parts[1]=="Monday":
			if parts[2] == "2022": return "January 3 2022"
			elif parts[2] == "2024": return "January 1 2024"
			else: return None
		else: return None