import scrapy
from alleco.objects.official import Official

class carnegie_b(scrapy.Spider):
	name = "carnegie_b"
	muniName = "CARNEGIE"
	muniType = "BOROUGH"
	complete = False

	def start_requests(self):
		urls = ['http://carnegieborough.com/government.html']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		#name, district, email, phone
		councilBits = [('p[1]//b/a/font','p[1]/font/font[2]/text()[1]','p[1]//b','p[1]/font/font[2]/text()[2]'),
						('p[2]//b/a/font','p[2]/font/font[2]/text()[1]','p[2]//b',None),
						('p[3]/b/','p[3]/font[1]//text()',None,'p[5]//text()'),
						('p[6]/font/span/','p[6]/font/font//text()','p[6]/','p[8]/font/font/text()'),
						('p[9]/b//a/font','p[9]/font[1]//text()','p[9]/','p[9]/span/text()'),
						('p[10]//span/a/','p[10]/font[2]/text()','p[10]//span','p[12]/font/text()')]
		for quote in response.xpath('//p[contains(font/font/b/text(),"Mayor")]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				name=quote.xpath("b/font/a/font/text()").get(),
				email=quote.xpath("b//a/@href").get(),
				phone=quote.xpath("font[2]/text()").getall()[-1],
				url=response.url)
		for quote in response.xpath('//td[contains(p/b/font/text(),"Borough of Carnegie Government")]/font'):
			for i in councilBits:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=quote.xpath("%s/text()" % i[0]).get(),
					district=quote.xpath(i[1]).get().upper().strip(),
					email=None if i[2]==None else quote.xpath("%s/a/@href" % i[2]).get(),
					phone=None if i[3]==None else quote.xpath(i[3]).get(),
					url=response.url)
	#### Additional Expected positions: 1 tax collector at-large
	#### Unable to be found on their website