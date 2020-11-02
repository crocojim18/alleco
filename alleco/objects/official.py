from scrapy.item import Item, Field

def getAllText(quote):
	return [i.replace("\xa0"," ").strip() for i in quote.xpath(".//text()").getall() if len(i.replace("\xa0"," ").strip())>0]

class Official(Item):
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