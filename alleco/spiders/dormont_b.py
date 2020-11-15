import scrapy
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class dormont_b(scrapy.Spider):
	name = "dormont_b"
	muniName = "DORMONT"
	muniType = "BOROUGH"
	complete = False

	def start_requests(self):
		urls = ['http://boro.dormont.pa.us/home/borough-council/',
		'http://boro.dormont.pa.us/meet-the-mayor/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-2] == "r":
			for quote in response.xpath('//article[@id="post-137"]'):
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=quote.xpath("h1/text()").get().split("–")[-1],
					email=quote.xpath('div/div[2]/p[2]/a/@href').get(),
					url=response.url)
		elif response.url[-2] == "l":
			for quote in response.xpath('//div[@class="entry-content"]'):
				fullNames = getAllText(quote.xpath("div"))
				emails = [(i.xpath("a/text()").get(),i.xpath("a/@href").get()) for i in quote.xpath("p")]
				names = {i[0].split(" ")[-1]:{"name":None,"email":i[1]} for i in emails}
				for i in fullNames:
					if i.split(" ")[-1] in names: names[i.split(" ")[-1]]["name"] = " ".join(i.split(" ")[-2:])
				#first name taken from 2019 election returns; was not on website when spider was first made
				if names["Moore"]["name"]==None: names["Moore"]["name"] = "John Moore"
				print(names)
				for person in names:
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="MEMBER OF COUNCIL",
						name=names[person]["name"],
						email=names[person]["email"],
						url=response.url)
		## EXPECTED: Tax collector at-large
		## Unable to find person holding office on website
