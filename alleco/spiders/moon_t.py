import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class moon_t(scrapy.Spider):
	name = "moon_t"
	muniName = "MOON"
	muniType = "TOWNSHIP"
	complete = False

	def start_requests(self):
		urls = ['http://www.moontwp.com/your-government/board-of-supervisors.php',
		'http://www.moontaxoffice.us/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-1]=='p':
			namesdates = []
			emails = []
			for quote in response.xpath("//ul[@class='listnone']")[0:2]:
				namesdates.append(getAllText(quote)[1:])
			for quote in response.xpath("//li[contains(strong/text(),'ail:')]"):
				emails.append(quote.xpath('text()').get().strip())
			for i in range(5):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="SUPERVISOR",
					name=namesdates[0][i],
					email=emails[i],
					termEnd=namesdates[1][i],
					url=response.url)
		elif response.url[-1]=='/':
			for quote in response.xpath('//div[@id="mainContent"]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=" ".join(quote.xpath('p[1]/text()').get().strip().split(" ")[3:5]),
					phone=quote.xpath('text()').get(),
					address=", ".join(response.xpath("//div[@id='footer']/div/p/text()").getall()[-1].split(' · ')[1:3]),
					url=response.url)
		# INCOMPLETE
		# Expected offices: 3 auditors, unable to be found on website