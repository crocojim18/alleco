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
				'bridgeville_b', 'carnegie_b', 'castle_shannon_b', 'chalfant_b',
				'cheswick_b', 'churchill_b', 'clairton_c', 'collier_t', 'coraopolis_b',
				'crafton_b', 'crescent_t', 'dormont_b', 'dravosburg_b', 'duquesne_c',
				'east_deer_t', 'east_mckeesport_b',
				'franklin_park_b', 'hampton_t', 'ingram_b', 'mccandless_t', 'monroeville_b',
				'moon_t', 'mount_lebanon_t', 'north_fayette_t', 'penn_hills_t',
				'pennsbury_village_b', 'pittsburgh_c', 'pine_t', 'plum_b', 'robinson_t',
				'ross_t', 'scott_t', 'shaler_t', 'south_fayette_t', 'south_park_t',
				'upper_st_clair_t', 'whitehall_b', 'wilkinsburg_b']

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
			remove("results/%s_temp.csv" % spider)
			spiderStatus[mess_same].append(spider)
		else:
			spiderStatus[mess_diff].append(spider)
			#print("\t{}\n\t{}".format(Counter(tempList) - Counter(oldList),Counter(oldList) - Counter(tempList)))
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
		print("\t"+spiName)

#reset fill of spiders who may have been run before but are no longer
for child in root:
	for muni in child:
		if muni.attrib["id"] in spiderList and muni.attrib["id"] in spiderStatus[mess_same]:
			muni.attrib["fill"] = "#00FA9A"
		elif muni.attrib["id"] in spiderList and muni.attrib["id"] in spiderStatus[mess_none]:
			muni.attrib["fill"] = "#FCBA03"
		elif muni.attrib["id"] in spiderList:
			muni.attrib["fill"] = "#800000"
		elif muni.attrib["id"] not in spiderList:
			muni.attrib["fill"] = "white"

tree.write('alleco/supp_data/map.svg')