import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class franklin_park_b(scrapy.Spider):
	name = "franklin_park_b"
	muniName = "FRANKLIN PARK"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['https://www.franklinparkborough.us/204/Borough-Council',
				'https://www.franklinparkborough.us/284/Mayor',
				'https://www.franklinparkborough.us/237/Property-Tax']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if "Council" in response.url:
			for quote in response.xpath("//div[@class='fr-view']")[5:7]:
				for person in quote.xpath('.//li'):
					thing = getAllText(person)
					if len(thing)==4: thing = [thing[0]+thing[1]]+thing[2:]
					if 'Junior Council Person' not in thing[0]:
						yield Official(
							muniName=self.muniName,
							muniType=self.muniType,
							office="MEMBER OF COUNCIL",
							name=thing[0].split(",")[0],
							district=thing[0].split(",")[-1].strip().upper(),
							termEnd=thing[1],
							email=thing[2],
							url=response.url)
		elif "Mayor" in response.url:
			for quote in response.xpath("//div[contains(h2/text(),'Responsibilities')]/p[2]"):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=quote.xpath("text()").get().split(",")[0],
					termEnd=quote.xpath("text()[2]").get(),
					email=quote.xpath("a/@href").get(),
					url=response.url)
		elif "Tax" in response.url:
			for quote in response.xpath("//ol[contains(li/div/text(),'Real Estate Tax Collector')]"):
				address = getAllText(quote.xpath("li[2]/div[1]"))[2:]
				address = address[0]+", "+address[1]+" ".join(address[2:])
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="TAX COLLECTOR",
					name=quote.xpath("li[1]/h4/text()").get(),
					phone=quote.xpath("li[2]/div[3]/text()").get(),
					address=address,
					email=quote.xpath("li[1]/div/a/@href").get(),
					url=response.url)