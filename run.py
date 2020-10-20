from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from collections import Counter
from os.path import exists
from os import rename, remove
from json import loads
import xml.etree.ElementTree as ET

process = CrawlerProcess(get_project_settings())

spiderList = ['aleppo_t', 'aspinwall_b', 'avalon_b', 'baldwin_b',
				'baldwin_t', 'bell_acres_b', 'bellevue_b', 'ben_avon_b',
				'ben_avon_heights_b', 'bethel_park_b', 'blawnox_b', 'brackenridge_b',
				'braddock_b', 'braddock_hills_b', 'bradford_woods_b', 'brentwood_b',
				'bridgeville_b', 'castle_shannon_b']#, 'carnegie_b']

# all of the spiders in the project.
for spider in spiderList:
	process.crawl(spider)
process.start() # the script will block here until the crawling is finished

# checking for differences from previous versions
# considerations:
#	cannot assume items will be in the same order
#	all pieces must be present and equal in both versions; not more or less information than before

tree = ET.parse('alleco/supp_data/map.svg')
root = tree.getroot()

mess_same = "These files were the same ({}/{}):"
mess_diff = "These files were NOT the same ({}/{}):"
mess_noPrior = "No prior versions of these files existed ({}/{}):"
mess_noNew = "No new versions of these files existed ({}/{}):"
mess_none = "No versions of these files existed ({}/{}):"
spiderStatus = {mess_same: [],
				mess_diff: [],
				mess_noPrior: [],
				mess_noNew: [],
				mess_none: []}
for spider in spiderList:
	#check to see if the files exist
	tempThere = exists("results/%s_temp.csv" % spider)
	oldThere = exists("results/%s.csv" % spider)
	if tempThere and oldThere:
		tempFile = open("results/%s_temp.csv" % spider)
		tempList = tempFile.readlines()
		tempFile.close()
		oldFile = open("results/%s.csv" % spider)
		oldList = oldFile.readlines()
		oldFile.close()
		filesSame = Counter(tempList) == Counter(oldList)
		if filesSame:
			remove("results/%s.csv" % spider)
			rename("results/%s_temp.csv" % spider, "results/%s.csv" % spider)
			spiderStatus[mess_same].append(spider)
		else:
			spiderStatus[mess_diff].append(spider)
	elif tempThere:
		spiderStatus[mess_noPrior].append(spider)
		rename("results/%s_temp.csv" % spider, "results/%s.csv" % spider)
	elif oldThere:
		spiderStatus[mess_noNew].append(spider)
	else:
		spiderStatus[mess_none].append(spider)

for key in spiderStatus:
	print(key.format(len(spiderStatus[key]), len(spiderList)))
	for spiName in spiderStatus[key]:
		muniSvgs = [muni for child in root for muni in child if muni.attrib["id"] == spiName]
		if len(muniSvgs)==1:
			muniSvgs[0].attrib["fill"] = "#00FA9A" if key==mess_same else "#800000"
			print("\t"+spiName)
		else:
			print("\t"+spiName+" (map error)")

tree.write('alleco/supp_data/map.svg')