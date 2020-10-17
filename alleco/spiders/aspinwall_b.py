import scrapy
from alleco.objects.official import Official

def detox(string):
	return string.replace("\u200b"," ").replace("\u00a0"," ").strip()

class aspinwall_b(scrapy.Spider):
	name = "aspinwall_b"
	muniName = "ASPINWALL"
	muniType = "BOROUGH"

	def start_requests(self):
		urls = ['https://www.aspinwallpa.com/aspinwall-borough',
		'https://www.aspinwallpa.com/tax-page']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-1] == "h":
			for quote in response.xpath('//div[@id="comp-jf8d75h8"]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=quote.xpath("p[1]//text()").get(),
					email=quote.xpath("p[3]//text()").get(),
					url=response.url)
			for column in response.xpath('//h6[contains(span//text(),"COUNCIL MEMBERS")]/../../div')[1:4]:
				textbits = column.xpath('.//span[contains(@style,"text-decoration:underline")]//text()').getall()
				textbits = [detox(x) for x in textbits if len(detox(x))>0]
				for i in range(len(textbits)//2):
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="MEMBER OF COUNCIL",
						name=textbits[i*2],
						email=textbits[i*2+1],
						url=response.url)
		elif response.url[-1] == "e":
			for quote in response.xpath('//div[@id="comp-j589ncus"]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath("h6[3]//text()").get().split("-")[1],
					email=quote.xpath("h6[5]//text()").get(),
					phone=quote.xpath("h6[4]//text()").get(),
					url=response.url)
