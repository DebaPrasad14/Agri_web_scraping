__author__ = "Deba M"
__Date__   = "09-MAY-2019"

import requests
from bs4 import BeautifulSoup
import pandas as pd


parent_url = "http://www.agriculture.gov.au"
request = requests.get("http://www.agriculture.gov.au/pests-diseases-weeds/plant#identify-pests-diseases")
content = request.text


soup = BeautifulSoup(content,"html.parser")
elements = soup.find_all(href = True)
pattern = "/pests-diseases-weeds/plant/"
un_nes = ['xylella/', 'national', 'quarantine/']
urls = []

for e in elements:
    if pattern in e['href']:
        if any(x in e['href'] for x in un_nes):
            pass
        else:
            urls.append(parent_url+ e['href'])

urls = list(set(urls))

records = []    # New list to append disease_name,img_url, origin, identity, specimen and what can came in to AUS for a
                # particular disease


for url in urls:
    request1 = requests.get(url)
    content1 = request1.text
    soup1 = BeautifulSoup(content1,"html.parser")

    dname = soup1.find_all('h2')[0].text
    img =parent_url + soup1.find_all('img')[3]['src']
    origin = soup1.find_all('strong')[1].next_sibling
    identity = soup1.find_all('strong')[3].next_sibling
    come_outof_aus = soup1.find_all("div", {"class":"hide"})[1].text
    specimen = soup1.find_all("div", {"class":"hide"})[2].text

    records.append([dname, img, origin, identity, come_outof_aus, specimen])


df = pd.DataFrame(records, columns=['Disease Name', 'Image Link', 'Origin', 'identification_of_pest', 'what can legally come into Australia', 'Secure any suspect specimens'])
df.to_csv('Agri_scrap.csv', index = False, encoding='utf-8-sig')     # writing data to csv/excel
df    # printing data in tabular form
