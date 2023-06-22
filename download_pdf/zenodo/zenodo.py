# example for upm

import json
import requests


query = "UPM" # UPM
page_size = 1000 # 
page = 1 # min 1
record_type = "software" # publication, software

basic_url = "https://zenodo.org/api/records/"

url = basic_url + "?q=" + query+ "&type=" + record_type + "&page" + str(page) + "&size=" + str(page_size)

r = requests.get(url).json()

json.dump(r['hits'], open(f"apis/zenodo/{record_type}.json", "w"), indent=4)