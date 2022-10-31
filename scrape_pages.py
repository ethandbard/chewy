from chewy_functions import *

# populates prod_links from textfile
LoadLinks("chewy\chewy_links_test.txt")

#get data from each page
ScrapePages(prod_links[0:2])

#save dict to json
prod_json = json.dumps(prod_dict, indent = 4)

#write .json 
SaveJson(prod_json, "chewy\\test_dump.json")