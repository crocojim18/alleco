import scrapy
from alleco.objects.official import Official
from re import split

class chalfant_b(scrapy.Spider):
	name = "chalfant_b"
	muniName = "CHALFANT"
	muniType = "BOROUGH"
	complete = True

	def start_requests(self):
		urls = ['http://chalfantborough-pa.org/government/borough-council/']
		for url in urls:
			yield scrapy.Request(url=url, 
				callback=self.parse, 
				headers={
				'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.84 Safari/537.36'
				})

	def parse(self, response):
		phone=response.xpath('//div[@class="pf-content"]/p[2]/text()').get().split(" ")[-1]
		councilBits = [("p[6]","div[2]"),("p[8]","p[9]"),
						("p[11]","p[12]"),('p[15]','div[6]'),
						('p[17]','p[18]'),('p[21]','p[23]'),('p[26]','p[27]')]
		for quote in response.xpath('//div[@class="pf-content"]'):
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="MAYOR",
				name=" ".join(quote.xpath("p[3]/text()").get().split(" ")[1:3]),
				phone=phone,
				email="".join(quote.xpath("p[4]/text()").getall()),
				url=response.url)
			for i in councilBits:
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					name=self._nameClean(quote.xpath("%s/text()" % i[0]).get()),
					phone=phone,
					email="".join(quote.xpath("%s//text()" % i[1]).getall()),
					url=response.url)
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="TAX COLLECTOR",
				name=" ".join(quote.xpath("p[35]/text()").get().split(" ")[1:3]),
				phone=phone,
				email=quote.xpath("p[36]/a/text()").get(),
				url=response.url)

	def _nameClean(self, string):
		toRet = []
		pieces = split(r"\s+",string)
		if pieces[0][-1]==".":
			pieces = pieces[1:]
		for word in pieces:
			if word[0]=="(":
				break
			toRet.append(word)
		return " ".join(toRet)