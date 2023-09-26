from chewy_functions import *

# populates prod_links from textfile
load_links("chewy_links_test.txt")

# get data from each page
scrape_pages(prod_links[0:2])

# save dict to json
prod_json = json.dumps(prod_dict, indent=4)

# write .json
save_json(prod_json, "data.json")
