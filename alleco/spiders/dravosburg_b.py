import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class dravosburg_b(scrapy.Spider):
	name = "dravosburg_b"
	muniName = "DRAVOSBURG"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['https://www.dravosburg.org/borough-officials']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		for quote in response.xpath('//div[@data-mesh-id="Containerc1qrainlineContent-gridContainer"]'):
			folks = []
			temp = []
			texto = getAllText(quote)
			for i in texto:
				if i.isupper():
					if len(temp)>0: folks.append(temp)
					temp = [i]
				else:
					temp.append(i)
			for person in folks:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL" if person[0] not in ["MAYOR","TAX COLLECTOR"] else person[0],
					phone=None if len(person)<3 else person[2] if "(" in person[2] else None,
					name=person[1],
					url=response.url)
