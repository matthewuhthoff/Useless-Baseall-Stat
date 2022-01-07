import pandas as pd
import requests
from bs4 import BeautifulSoup
from enum import Enum

class stats(Enum):
    plateAppearences = 0
    runs = 1
    hits = 2
    doubles = 3
    triples = 4
    homeRuns = 5
    stolenBases = 6
    caughtStealing = 7
    basesOnBalls = 8
    strikeOuts = 9
    groundIntoDoublePlay = 10
    hitByPitch = 11




class Hitter(object):
    hitter_stats = []
    funStat = None
    funStat_plus = None
    name = None
    temper = None
    active = 1


    def __init__(self, URL):
        result = requests.get(URL)
        src = result.content
        soup = BeautifulSoup(src, 'lxml')
        
        self.getName(soup)
        self.populate_stats(URL)
        self.calc_funstat()

    def getName(self, soup):
        self.name = soup.find("h1").text
        self.name = self.name.strip("\n")


    def populate_stats(self, URL):
        df = pd.read_html(URL) 
        data_frame = df[0]
        rows = data_frame.shape[0]
        i = 0
        for i in range (rows):
            try:
                if pd.isnull(data_frame.iat[i,0]):
                    continue
                if data_frame.iat[i,0] == '2021':
                    break
            except IndexError as error:
                pass
        row = i
        self.temper = data_frame.iat[row, 5]
        temp_list = []
        temp_list.append(data_frame.iat[row,5])
        temp_list.append(data_frame.iat[row,7])
        temp_list.append(data_frame.iat[row,8])
        temp_list.append(data_frame.iat[row,9])
        temp_list.append(data_frame.iat[row,10])
        temp_list.append(data_frame.iat[row,11])
        temp_list.append(data_frame.iat[row,13])
        temp_list.append(data_frame.iat[row,14])
        temp_list.append(data_frame.iat[row,15])
        temp_list.append(data_frame.iat[row,16])
        temp_list.append(data_frame.iat[row,23])
        temp_list.append(data_frame.iat[row,24])
        self.hitter_stats = temp_list
        
    def calc_funstat(self):
        self.funStat = 0
        try:
            self.funStat += 2 * int(float(self.hitter_stats[stats.doubles.value]))
            self.funStat += 3 * int(float(self.hitter_stats[stats.triples.value]))
            self.funStat += int(float(self.hitter_stats[stats.runs.value]))
            self.funStat += 4 * int(float(self.hitter_stats[stats.homeRuns.value]))
            self.funStat += 2 * int(float(self.hitter_stats[stats.stolenBases.value]))
            self.funStat += 2 * int(float(self.hitter_stats[stats.caughtStealing.value]))
            self.funStat -= int(float(self.hitter_stats[stats.basesOnBalls.value]))
            self.funStat -= int(float(self.hitter_stats[stats.strikeOuts.value]))
            self.funStat += 3 * int(float(self.hitter_stats[stats.groundIntoDoublePlay.value]))
            self.funStat += 3 * int(float(self.hitter_stats[stats.hitByPitch.value]))
            self.funStat /= int(float(self.hitter_stats[stats.plateAppearences.value]))
            if self.hitter_stats[stats.plateAppearences.value] < 150:
                self.active = 0
        except:
            self.active = 0
