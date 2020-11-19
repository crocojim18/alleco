# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from re import sub
from re import search
from re import I
from scrapy.exporters import CsvItemExporter


def cleanItem(string):
	if string==None: return None
	string = string.strip()
	string = sub("(\u2018|\u2019)", "'", string)
	string = sub("(\u201C|\u201D)", '"', string)
	string = sub("\xa0", " ", string)
	if string[0:7] == "mailto:": string = string[7:]
	return sub(r"\s+", " ", string)

def cleanPhone(string):
	if string==None: return None
	string = cleanItem(string)
	match = search(r"(\d{3})[\) \-–]{0,2}(\d{3})[ \-–]{0,3}(\d{4})[, ]{0,2}(ext(ension|.)? | ?x ?)?(?P<ext>\d+)?", string, I)
	if match == None: return string
	else:
		ending = "" if match.group("ext")==None else "p"+match.group("ext")
		return match[1]+match[2]+match[3]+ending

def cleanDatesNumeric(string):
	if string==None: return None
	match = search(r"(?P<month>\d{1,2})[-/]((?P<date>\d{1,2})[/-])?(?P<year>\d{2,4})", string)
	if match == None: return string
	else:
		toRet = ""
		yearInt = int(match.group("year"))
		if yearInt < 100:
			if yearInt < 50: yearInt += 2000
			else: yearInt += 1900
		toRet = str(yearInt)
		monthInt = int(match.group("month"))
		toRet += "-"+("" if monthInt>9 else "0")+str(monthInt)
		if match.group("date")!=None and int(match.group("date"))<=31:
			dateInt = int(match.group("date"))
			toRet += "-"+("" if dateInt>9 else "0")+str(dateInt)
		return toRet

def cleanDates(string):
	if string==None: return None
	string = cleanItem(string)
	months = ["January","February","March","April","May","June",
				"July","August","September","October","November","December"]
	match = search("(?P<month>{})".format("|".join(months))+r"? ?(?P<date>\d{1,2})?,? ?(?P<year>\d{4})", string)
	if match == None: return cleanDatesNumeric(string)
	else:
		toRet = ""
		toRet = match.group("year")
		if match.group("month")!=None and match.group("month") in months:
			monthInt = next(x for x in range(len(months)) if months[x] == match.group("month"))+1
			toRet += "-"+("" if monthInt>9 else "0")+str(monthInt)
		if match.group("date")!=None and int(match.group("date"))<=31:
			dateInt = int(match.group("date"))
			toRet += "-"+("" if dateInt>9 else "0")+str(dateInt)
		return toRet

class AllecoPipeline:
	def process_item(self, item, spider):
		item["name"] = cleanItem(item["name"])
		if "email" in item: item["email"] = cleanItem(item["email"])
		if "phone" in item: item["phone"] = cleanPhone(item["phone"])
		if "termStart" in item: item["termStart"] = cleanDates(item["termStart"])
		if "termEnd" in item: item["termEnd"] = cleanDates(item["termEnd"])
		if "address" in item: item["address"] = cleanItem(item["address"])
		return item

class CsvExportPipeline:
	def __init__(self):
		self.file = None
		self.exporter = None

	def open_spider(self, spider):
		if spider.complete:
			self.file = open("results/%s_temp.csv" % spider.name, 'wb')
			self.exporter = CsvItemExporter(self.file)
			self.exporter.start_exporting()

	def close_spider(self, spider):
		if spider.complete:
			self.exporter.finish_exporting()
			self.file.close()

	def process_item(self, item, spider):
		self._setDefaults(item)
		if spider.complete:
			self.exporter.export_item(item)
		return item

	def _setDefaults(self,item):
		item.setdefault("district", "AT-LARGE")
		item.setdefault("email", None)
		item.setdefault("phone", None)
		item.setdefault("address", None)		
		item.setdefault("termStart", None)
		item.setdefault("termEnd", None)
		item.setdefault("vacant", False)
