import scrapy
from alleco.objects.official import Official

class clairton_c(scrapy.Spider):
	name = "clairton_c"
	muniName = "CLAIRTON"
	muniType = "CITY"
	complete = True

	def start_requests(self):
		urls = ['http://cityofclairton.com/clairton-city-council/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		councilNums = [2,3,4,5]
		for quote in response.xpath('//article[@id="post-551"]/div[1]'):
			mayor = {"name": quote.xpath("div[1]/strong/text()").get(),
				"phone": quote.xpath("div[4]/text()").get(),
				"url": response.url}
			req = scrapy.Request(url="http://cityofclairton.com/mayor-of-clairton/",
				callback=self.mayorParse, cb_kwargs=mayor)
			yield req
			for num in councilNums:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=quote.xpath(".//strong/text()").getall()[num-1],
					phone=quote.xpath(".//div[contains(text(),'Phone:')]/text()").getall()[num-1],
					email=None if num!=2 else quote.xpath(".//a/@href").get(),
					district=quote.xpath(".//em/text()").getall()[num-1].split("–")[1].strip().upper(),
					url=response.url)

	def mayorParse(self, response, name, phone, url):
		for quote in response.xpath('//article[@id="post-550"]/div[1]/p[1]'):
			mayor = Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				name=name,
				phone=phone,
				email=quote.xpath("a/@href").get(),
				url=url)
			yield mayor
