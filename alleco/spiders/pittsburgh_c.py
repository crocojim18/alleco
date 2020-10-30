import scrapy
from alleco.objects.official import Official
from re import search

class pittsburgh_c(scrapy.Spider):
	name = "pittsburgh_c"
	muniName = "PITTSBURGH"
	muniType = "CITY"
	complete = True

	def start_requests(self):
		urls = ['https://pittsburghpa.gov/mayor/mayor-contact',
		'https://pittsburghpa.gov/controller/controller-contact']
		urls += ["https://pittsburghpa.gov/council/d{}-contacts".format(i+1) for i in range(9)]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		if "/mayor/" in response.url:
			for quote in response.xpath('//*[@class="contacts-content"]'):
				parts = [x.strip() for x in quote.xpath(".//text()").getall() if len(x.strip())>1]
				alldict = self._getall(parts)
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MAYOR",
					name=alldict["name"],
					address=alldict["address"],
					url=response.url)
		elif "/controller/" in response.url:
			for quote in response.xpath('//*[@class="contacts-content"]'):
				parts = [x.strip() for x in quote.xpath(".//text()").getall() if len(x.strip())>1]
				alldict = self._getall(parts)
				req = scrapy.Request(url="https://pittsburghpa.gov/controller/controller-bio",
					callback=self.controllerParse, cb_kwargs=alldict)
				yield req
		elif "/council/" in response.url:
			existed = False
			for quote in response.xpath('//*[@class="contacts-content" and contains(., "Council")]')[0:1]:
				existed = True
				parts = [x.strip() for x in quote.xpath(".//text()").getall() if len(x.strip())>1]
				alldict = self._getall(parts)
				if response.url[-10] == '8':
					tempAddr = [x.strip() for x in response.xpath('//*[@class="contacts-content"][1]//text()').getall() if x.strip()!='']
					alldict["address"] = self._address(tempAddr[1:4])
				elif response.url[-10] == '7':
					tempEmail = [x.strip() for x in response.xpath('//*[@class="contacts-content"]')[1:2].xpath('.//text()').getall() if x.strip()!='']
					alldict["email"] = self._email(tempEmail)
				elif response.url[-10] == '6':
					tempPhone = [x.strip() for x in response.xpath('//*[@class="contacts-content"]')[1:2].xpath('.//text()').getall() if x.strip()!='']
					alldict["phone"] = self._phone(tempPhone)
				yield Official(
					muniName=self.muniName,
					muniType=self.muniType,
					office="MEMBER OF COUNCIL",
					district="DISTRICT {}".format(response.url[-10]),
					name=alldict["name"],
					address=alldict["address"],
					phone=alldict["phone"],
					email=alldict["email"],
					url=response.url)
			if not existed:
				for quote in response.xpath('//div[@class="col-md-6"]'):
					parts = [x.strip() for x in quote.xpath(".//text()").getall() if len(x.strip())>1][5:10]
					alldict = self._getall(parts)
					yield Official(
						muniName=self.muniName,
						muniType=self.muniType,
						office="MEMBER OF COUNCIL",
						district="DISTRICT {}".format(response.url[-10]),
						name=alldict["name"],
						address=alldict["address"],
						phone=alldict["phone"],
						email=alldict["email"],
						url=response.url)

	def _getall(self, parts):
			name = self._name(parts.pop(0))
			email = self._email(parts)
			self._fax(parts)
			phone = self._phone(parts)
			address = self._address(parts)
			return {"name":name,"email":email,"phone":phone,"address":address}

	def _name(self, string):
		toRet = ""
		string = string.split(" ")
		for i in range(len(string)):
			if string[-(i+1)] in ["President","Councilman","Councilwoman","Mayor","Controller"]:
				break
			toRet = string[-(i+1)] + " " + toRet
		return toRet

	def _email(self, parts):
		toRet = None
		for i in range(len(parts)):
			if "@" in parts[i]:
				toRet = parts.pop(i)
				break
		for i in range(len(parts)):
			if "E-Mail" in parts[i]:
				parts.pop(i)
				break
		return toRet

	def _fax(self, parts):
		for i in range(len(parts)):
			if "Fax" in parts[i]:
				parts.pop(i)
				break
		return None

	def _phone(self, parts):
		for i in range(len(parts)):
			if search(r"\d-\d",parts[i])!=None:
				return parts.pop(i)
		return None

	def _address(self, parts):
		suitepart = None
		for i in range(len(parts)):
			if "Suite" in parts[i]:
				suitepart = i
				break
		if suitepart!=None: parts.insert(1, parts.pop(suitepart))
		toRet = ", ".join(parts)
		return toRet

	def controllerParse(self, response, address, phone, email, name):
		for quote in response.xpath('//div[@class="col-md-12"]')[2:3]:
			yield Official(
				muniName=self.muniName,
				muniType=self.muniType,
				office="CONTROLLER",
				name=self._name(quote.xpath("h1/text()").get()),
				address=address,
				phone=phone,
				email=email,
				url=response.url)