import scrapy, re
from alleco.objects.official import Official

class avalon_b(scrapy.Spider):
	name = "avalon_b"
	muniName = "AVALON"
	muniType = "BOROUGH"

	def start_requests(self):
		urls = ['http://www.boroughofavalon.org/officials.html']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		self.phone=self._phone(response)
		councilWards = {"1": ["p[40]","p[41]","p[42]"],
						"2": ["p[44]","div[8]"],
						"3": ["p[48]","div[9]/p[1]","div[9]/p[2]"]}
		for quote in response.xpath('//div[@id="wb_element_text__1261203424171_36"]/div'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				phone=self.phone,
				name=quote.xpath("p[35]//text()").get(),
				email=quote.xpath("p[36]//a/@href").get().split(":")[1],
				url=response.url)
		for wards in councilWards:
			for nums in councilWards[wards]:
				for quote in response.xpath('//div[@id="wb_element_text__1261203424171_36"]/div'):
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						phone=self.phone,
						office="MEMBER OF COUNCIL",
						district="WARD %s" % wards,
						name=quote.xpath("%s//text()" % nums).get().split("(")[0],
						email=quote.xpath('%s//a[contains(.//text(),"Email")]/@href' % nums).get(),
						url=response.url)
		for quote in response.xpath('//div[@id="wb_element_text__1261203424171_36"]/div'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				phone=self.phone,
				office="MEMBER OF COUNCIL",
				district="WARD 2",
				name=quote.xpath("p[45]//text()").get().split("(")[0],
				email=quote.xpath('p[45]/a/@href').get().split(":")[1],
				url=response.url)
		for quote in response.xpath('//div[@id="wb_element_text__1261203424171_36"]/div'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				phone=self.phone,
				office="TAX COLLECTOR",
				name=quote.xpath("div[9]/p[5]//text()").get().split("(")[0],
				url=response.url)

	def _phone(self, response):
		string = response.xpath('//div[@id="wb_element_text__1261203424171_36"]/div/p[1]//text()').get()
		string = string.split(" ")[6]
		return string