# example for upm

import json
from asyncio import sleep

import requests


institution = "I88060688" # I88060688 = UPM
per_page = 200 # max 200 min 1

basic_url = "https://api.openalex.org/works?filter=institutions.id:"

url = basic_url + institution + "&per-page=" + str(per_page)

total_works = requests.get(basic_url + institution).json()['meta']['count']

iteractions = int(total_works / per_page)+1
print(iteractions)
works = []

for i in range(iteractions+1):
    try:
        print(i)
        if i == 0 :
            final_url = url + "&cursor=*"
            data = requests.get(final_url).json()
            next_cursor = data['meta']['next_cursor']
            works = works + data['results']# change to continue if you want to get all the works
        final_url = url + "&cursor=" + next_cursor
        data = requests.get(final_url).json()
        next_cursor = data['meta']['next_cursor']
        works = works + data['results']
        sleep(1)
    except Exception as e:
        print("error")
        print(str(e))
        pass

# for j in works:
#     print(j['title'], j['id'],j['doi'])
#     break
json.dump(works, open("./works.json", "w+"), indent=4)