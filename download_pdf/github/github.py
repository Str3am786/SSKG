import json
import requests

basic_url = r"https://api.github.com/search/repositories?"

per_page = 100
upm_url = basic_url+r"q=Universidad%20politecnica%20de%20madrid+in:name,description,readme&per_page="+str(per_page)

results = requests.get(upm_url).json()
total_count = results['total_count']
print('Total count: ', total_count)

iteractions = int(total_count / per_page) + 1

repos = results['items']
print('-'*50)
for i in range(2,iteractions+1):
    final_url = upm_url + "&page=" + str(i)
    data = requests.get(final_url).json()
    repos = repos + data['items']
    print(i,len(repos))

    

json.dump(repos, open("apis/github/repos.json", "w"), indent=4)