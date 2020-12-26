from scrapy.item import Item, Field

def getAllText(quote):
	"""
	Returns cleaned text from a parsed node.
	Removes non-breaking spaces (\xa0) & extra whitespace.
	"""
	return [i.replace("\xa0"," ").strip()
			for i in quote.xpath(".//text()").getall()
			if len(i.replace("\xa0"," ").strip())>0]

def getTextOfType(quote, htmltype):
	"""
	Returns cleaned text from a parsed node that descends from the given type.
	Removes non-breaking spaces (\xa0) & extra whitespace.
	"""
	return [i.replace("\xa0"," ").strip()
			for i in quote.xpath(".//%s//text()" % htmltype).getall()
			if len(i.replace("\xa0"," ").strip())>0]

def getAllLinks(quote):
	"""
	Returns all links in the given node
	"""
	return [i for i in quote.xpath(".//a/@href").getall()]

class Official(Item):
	"""
	Object type for municipal officials. Inherits Scrapy Item functions.

	Parameters
	----------
	self.muniName : name of municipality
	self.muniType : type of municipality (borough, township, city)
	self.office : name of office
	self.district : official's ward, district, or other internal division. defaults to AT-LARGE
	self.name : official's name
	self.email : official's email
	self.phone : official's phone number
	self.address : official's address
	self.url : response.url for prior info
	self.termStart : start date of official's term in office, string in ISO format
	self.termEnd : end date of official's term in office, string in ISO
	self.vacant : position status, boolean value

	Attributes
    ----------
	self.setdefault() : assigns values
	"""

	muniName = Field()
	muniType = Field()
	office = Field()
	district = Field()
	name = Field()
	email = Field()
	phone = Field()
	address = Field()
	url = Field()
	termStart = Field()
	termEnd = Field()
	vacant = Field()

	def setdefault(self, key, value):
		if key not in self:
			self[key] = value
