import csv, sys, re

muni = " ".join(sys.argv[1:])
temp2017 = open("alleco/supp_data/2017_gen.csv", newline='')
csv2017 = [x for x in csv.reader(temp2017)]
temp2017.close()
for line in [bit for bit in csv2017 if re.search(muni, bit[1], re.I)!=None]:
	print("(2017) {}: {}".format(line[1], line[2]))
temp2019 = open("alleco/supp_data/2019_gen.csv", newline='')
csv2019 = [x for x in csv.reader(temp2019)]
temp2019.close()
for line in [bit for bit in csv2019 if re.search(muni, bit[1], re.I)!=None]:
	print("(2019) {}: {}".format(line[1], line[2]))