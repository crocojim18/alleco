from scrapy.item import Item, Field

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