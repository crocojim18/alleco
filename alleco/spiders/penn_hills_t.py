import scrapy, re
from alleco.objects.official import Official

class penn_hills_t(scrapy.Spider):
	name = "penn_hills_t"
	muniName = "PENN HILLS"
	muniType = "TOWNSHIP"
	complete = True

	def start_requests(self):
		urls = ['https://pennhills.org/government-contacts/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//div[@class="et_pb_row et_pb_row_2"]/div')[0:2]:
			alltext = [x.strip() for x in quote.xpath(".//text()").getall() if len(x.strip())>0]
			if alltext[0]=="Mayor": yield self._member(alltext[1:], response.url,"MAYOR")
			else: yield self._member(alltext[1:], response.url)
		for quote in response.xpath('//div[@class="et_pb_row et_pb_row_4"]/div'):
			alltext = [x.strip() for x in quote.xpath(".//text()").getall() if len(x.strip())>0]
			yield self._member(alltext, response.url)
		for quote in response.xpath('//div[@class="et_pb_row et_pb_row_5"]/div')[0:1]:
			alltext = [x.strip() for x in quote.xpath(".//text()").getall() if len(x.strip())>0]
			yield self._member(alltext[1:], response.url,"CONTROLLER")

	def _member(self, textarr, url, office="MEMBER OF COUNCIL"):
		phone = textarr[1]
		name = textarr[0]
		email = None if len(textarr)<4 else textarr[3]
		return Official(
			muniName=self.muniName,
			muniType=self.muniType,
			office=office,
			phone=phone,
			name=name,
			email=email,
			url=url)
