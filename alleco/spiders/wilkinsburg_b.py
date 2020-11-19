import scrapy, re
from alleco.objects.official import Official
from alleco.objects.official import getAllText

class wilkinsburg_b(scrapy.Spider):
	name = "wilkinsburg_b"
	muniName = "WILKINSBURG"
	muniType = "BOROUGH"
	complete = False

	def start_requests(self):
		urls = ['https://www.wilkinsburgpa.gov/your-government/borough-council/',
		'https://www.wilkinsburgpa.gov/your-government/welcome/']
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if response.url[-2]=='l':
			for quote in response.xpath('//article[@id="post-346"]'):
				bits = getAllText(quote)
				peeps = []
				peeps.append(bits[8:10])
				peeps.append([bits[10],bits[14]])
				peeps.append(bits[15:17])
				peeps.append([bits[15],bits[20],bits[23]])
				peeps.append(bits[24:26])
				peeps.append([bits[24]]+bits[27:30])
				peeps.append(bits[31:34])
				peeps.append([bits[31],bits[34]])
				peeps.append([bits[31]]+bits[-2:])
				for i in peeps:
					yield self._member(i,response)
		elif response.url[-2]=='e':
			for quote in response.xpath('//article[@id="post-343"]'):
				bits = quote.xpath("p[16]/text()").get()
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					email=bits.strip().split(" ")[-1],
					name=quote.xpath("h3[2]/text()").get(),
					phone=bits,
					url=response.url)
		#EXPECTED OFFICERS: ONE TAX COLLECTOR AT-LARGE

	def _member(self,person,response):
		ward = re.search(r"([a-z1-3]+?) ward",person[0],re.I)
		if ward[1] in ["1st", 'First']: ward = "WARD 1"
		elif ward[1] in ["2nd", "Second"]: ward = "WARD 2"
		elif ward[1]=="Third": ward = "WARD 3"
		name = ""
		if "," in person[0]: name = person[0].split(",")[0]
		else: name = person[1].split("(")[0]
		email = None
		phone = None
		for possEmails in person:
			possPhone = re.search(r"\(?\d{3}\)?[ \-–]\d{3} ?[–\-] ?\d{4}",possEmails)
			if possPhone != None:
				phone = possPhone[0]
			for words in possEmails.split(" "):
				if "@" in words: email = words
		return Official(
			muniName=self.muniName,
			muniType=self.muniType,
			office="MEMBER OF COUNCIL",
			district=ward,
			email=email,
			name=name,
			phone=phone,
			url=response.url)
