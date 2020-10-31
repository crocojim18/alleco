import scrapy
from alleco.objects.official import Official
from re import split

class mount_lebanon_t(scrapy.Spider):
	name = "mount_lebanon_t"
	muniName = "MOUNT LEBANON"
	muniType = "TOWNSHIP"
	complete = True
	comAddress = ""

	def start_requests(self):
		urls = ['https://mtlebanon.org/28/Commissioners',
		'https://mtlebanon.org/62/Tax-Office']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-1]=='e':
			for quote in response.xpath("//li[@class='InfoAdvanced widgetItem ']")[0:1]:
				bits = [x.strip() for x in quote.xpath("text()").getall() if len(x.strip())>0]
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TREASURER",
					name=quote.xpath("span[1]/text()").get(),
					address=bits[3]+", "+bits[4],
					phone=bits[5],
					url=response.url)
		elif response.url[-1]=='s':
			addr = response.xpath("//div[@id='divEditor369e008b-89c1-44c3-9afe-c47cabcfe8eb']/text()").getall()[-2:]
			self.comAddress = ", ".join(addr)
			for quote in response.xpath("//div[@id='divEditor369e008b-89c1-44c3-9afe-c47cabcfe8eb']/a")[3:8]:
				url = response.urljoin(quote.xpath('./@href').get())
				req = scrapy.Request(url=url, callback=self.councilParse)
				yield req

	def councilParse(self, response):
		for quote in response.xpath("//ul[contains(li/a/text(),'Contact Com')]"):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				district=response.xpath('//h1[@id="versionHeadLine"]/text()').get().upper().strip(),
				office="COMMISSIONER",
				name=split('Commissioner',response.xpath('//h2[contains(text(),"Contact ")]/text()').get())[-1],
				phone=quote.xpath('li[1]/text()').get(),
				termEnd=quote.xpath('li[2]/text()').get(),
				email=quote.xpath('li[3]/a/@href').get(),
				address=self.comAddress,
				url=response.url)