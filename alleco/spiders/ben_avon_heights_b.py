import scrapy
from alleco.objects.official import Official

class ben_avon_heights_b(scrapy.Spider):
	name = "ben_avon_heights_b"
	muniName = "BEN AVON HEIGHTS"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['http://www.benavonheightsborough.com/borough/index.html',
		'http://www.benavonheightsborough.com/community/community-faq.html']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-6] == "x":
			for quote in response.xpath('//tr[contains(th/text(),"Mayor")]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=quote.xpath("td/text()").get().split("(")[0],
					url=response.url)
			for line in response.xpath('//tr[contains(th/text(),"Council Members")]/td/text()').getall():
				for name in [x for x in line.split(",") if len(x.strip())>0]:
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="MEMBER OF COUNCIL",
						name=name,
						url=response.url)
		elif response.url[-6] == "q":
			for quote in response.xpath('//div[@id="FAQ7ans"]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=" ".join(quote.xpath("./text()").get().strip().split(" ")[0:2]),
					url=response.url)
