import requests
import json
import os
import matplotlib.pyplot as plt

EXCLUDE_REPOS = ["dwm","st"]

#pat = ""

#with open("../gh_pat_for_content_readonly","r") as f:
#	pat = f.read().strip()

pat = os.environ["METADATA_PAT"]


# Get list of all repos
resp = json.loads(requests.get("https://api.github.com/user/repos",headers={"Authorization":f"Bearer {pat}"}).text)
repos = [i.get("name") for i in resp if i.get("name") not in EXCLUDE_REPOS]

result = dict()

# Get Languages for individual repos
for repo_name in repos:
	lang = json.loads(requests.get(f"https://api.github.com/repos/Night-fury0/{repo_name}/languages",headers={"Authorization": f"Bearer {pat}"}).text)
	for i in  lang:
		if i not in result:
			result[i] = lang[i]
		else:
			result[i] += lang[i]


# Generate Pie Chart
result = dict(sorted(result.items(), key=lambda x:x[1], reverse=True))
labels = list(result.keys())
sizes = list(result.values())
total = sum(sizes)
explode = [0] * len(labels)

fig, ax = plt.subplots(figsize=(10,4))
fig.set_facecolor(("grey"))
widgets, texts, autotexts = ax.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', startangle=90, labeldistance=1.06, pctdistance=0.8)
plt.title("Languages Used in Repos",bbox={'facecolor':'0.8', 'pad':5})

threshold = 10

for label, pct_label in zip(texts, autotexts):
    pct_value = pct_label.get_text().rstrip('%')
    if float(pct_value) < threshold:
        label.set_text('')
        pct_label.set_text('')

labels = [f'{l} : {(100*result[l]/total):0.2f} %' for l in labels]
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.legend(labels, loc="best", bbox_to_anchor=(1.0,1.0))
plt.savefig('pie_chart.jpg',dpi=300)
