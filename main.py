import requests
from hit import Hitter
import requests
from bs4 import BeautifulSoup
import re
from googlesearch import search
import operator





result1 = requests.get('https://www.fantraxhq.com/fantasy-baseball-hitter-rankings/')
src1 = result1.content
soup1 = BeautifulSoup(src1, 'lxml')
rows1 = soup1.find_all("tr")
names = []
for row1 in rows1:
    cells = row1.findChildren('td')
    for cell in cells:
        if cell.attrs['class'] == ['column-2']:
            cell_content = cell.getText()
            if cell_content == "":
                continue
            clean_content = re.sub( '\s+', ' ', cell_content).strip()
            clean_content = clean_content + " baseball reference"
            names.append(clean_content)

player_list = {}


for q in range(len(names)):
    for URL in search(names[q], tld="co.in", num=1, stop=1, pause=2):
        temp = Hitter(URL)
        if temp.active == 1:
            player_list[temp.name] = temp
        del temp

league_funStat = 0
for key in player_list:
    league_funStat += player_list.get(key).funStat 
league_funStat /= len(player_list)

for key in player_list:
    player_list.get(key).funStat_plus = player_list.get(key).funStat / league_funStat * 100
    player_list.get(key).funStat_plus = round(player_list.get(key).funStat_plus)


temp_list = sorted(player_list.values(), key=operator.attrgetter('funStat_plus'), reverse=True)
for idx, player in enumerate(temp_list):
    print((idx + 1), ". ", player.name, ": ", player.funStat_plus)
