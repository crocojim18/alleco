import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText
from re import split

class shaler_t(scrapy.Spider):
	name = "shaler_t"
	muniName = "SHALER"
	muniType = "TOWNSHIP"
	complete = True

	def start_requests(self):
		urls = ['https://www.shaler.org/323/Shaler-Township-Elected-Officials']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//div[@id="divEditor909176e4-b373-45cd-af7f-deacc7efb43e"]/span'):
			parts = "  ".join(getAllText(quote))
			parts = [x for x in split(r"\s{2,}", parts)[4:] if x!="Vice President"]
			for i in range(7):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="COMMISSIONER",
					name=parts[i*6].split(",")[0],
					district=parts[i*6+1].upper(),
					termEnd=parts[i*6+3],
					phone=parts[i*6+5],
					address=parts[i*6+2]+", "+parts[i*6+4],
					url=response.url)
		for quote in response.xpath('//tr[@class="textContent"]')[0:1]:
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=quote.xpath("td[1]/text()").get(),
				termEnd=quote.xpath("td[4]/text()").get(),
				phone=quote.xpath("td[3]/div[3]/text()").get(),
				address=quote.xpath("td[3]/text()").get()+", "+quote.xpath("td[3]/div[1]/text()").get(),
				url=response.url)
	

