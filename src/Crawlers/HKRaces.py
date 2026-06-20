import os
import numpy as np

from bs4 import BeautifulSoup

from Crawlers.Races import *
from Helpers import WebHelper as wh


# url = "https://racing.hkjc.com/racing/information/English/racing/RaceCard.aspx?RaceDate={}&Racecourse={}&RaceNo={}".format(
#         date, venue, no)

class HKRaces(Races):
    def __init__(self):
        super().__init__()
        self.location = "HK"
        self.racecardurl = "https://racing.hkjc.com/racing/information/English/racing/RaceCard.aspx"
        self.racecardquery="?RaceDate={}&Racecourse={}&RaceNo={}"
        self.raceresulturl = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx"
        self.racereusltquery = "?RaceDate={}&Racecourse={}&RaceNo={}"
        self.racehorseurl = "https://racing.hkjc.com/en-us/local/information/selecthorsebychar"
        self.racehorsequery = "?ordertype={}"
        self.racehorsefileprefix = "RaceHorse"
        self.raceresultfileprefix = "RaceResult"
        self.racecardfileprefix = "RaceCard"
        self.venues = ['HV', 'ST']
        self.nos = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', ]
        self.numofHorse = 16

    def getResults(self, date):
        Results = []

        for venue in self.venues:
            for no in self.nos:
                query = self.racereusltquery.format(date, venue, no)
                url = self.raceresulturl + query
                content = wh.get_urlcontent(url)

                div = content.find_all('div', {'class': "performance"})
                if len(div) <= 0:
                    # print("No race in {1} on {0}!".format(date, venue))
                    break

                race = None
                horses, winner = self.extractResultHorses(div)
                if len(horses) > 0:
                    race = {}
                    race['date'] = date
                    race['venue'] = venue
                    race['race_no'] = no
                    race['horses'] = horses
                    race['win'] = winner

                if race == None:
                    break

                Results.append(race)

        return Results

    def getHorses(self):
        horses = []

        for code in range(ord('a'), ord('z') + 1):
            query = self.racehorsequery.format(chr(code))
            url = self.racehorseurl + query
            content = wh.get_urlcontent(url)

            links = content.find_all('a', {'class': "table_eng_text"})
            for i in range(len(links)):
                horse = links[i].get_text()
                horses.append(horse)

            print(f"{len(horses)} of horses read.")

        return horses

    def getCards(self, date):
        Cards = []

        for venue in self.venues:
            for no in self.nos:
                query = self.racecardquery.format(date.strftime('%Y/%m/%d'), venue, no)
                url = self.racecardurl + query
                content = wh.get_urlcontent(url)

                tab = content.find_all('table', {'id': "racecardlist"})
                if len(tab) <= 0:
                    print(f"No race more card found in {venue}!")
                    break

                race = None
                horses = self.extractCardHorses(tab)
                print(f"Race {no}: {len(horses)} horses")
                if len(horses) > 0:
                    race = {}
                    race['date'] = date
                    race['venue'] = venue
                    race['race_no'] = no
                    race['horses'] = horses

                if race != None:
                    Cards.append(race)

        return Cards

    def extractCardHorses(self, table):

        horses = []
        for t in table:
            rows = t.select('tr')
            for row in rows:
                trsoup = BeautifulSoup(str(row), 'html.parser')
                links = trsoup.find_all('a')

                linkcounter = 0
                for i in range(len(links)):
                    if i > 0:
                        break;
                    horse = links[i].get_text()
                    if horse not in horses:
                        horses.append(links[i].get_text())

        return horses

    def extractResultHorses(self, div):
        horses = [''] * self.numofHorse
        winner = ''

        divcounter = 0
        for d in div:
            if divcounter >= 1:
                break

            # print(d)
            rows = d.select('tr')
            divcounter = divcounter + 1
            rowcounter = 0

            for row in rows:
                rowcounter = rowcounter + 1
                if rowcounter == 1:
                    continue
                trsoup = BeautifulSoup(str(row), 'html.parser')

                td = trsoup.find_all('td')
                try:
                    horse_no = int(td[1].getText().strip()) -1
                except ValueError:
                    continue

                link = td[2].find_all('a', {'class': "local"})
                if 'horseid' in link[0]['href'].lower():
                    horses[horse_no] = link[0].getText()

                    if rowcounter == 2:
                        winner = link[0].getText()

                # links = trsoup.find_all('a', {'class': "local"})

                # for a in links:
                #    if 'horseid' in a['href'].lower():
                #        if rowcounter == 1:
                #            winner = a.getText()

                        # horses[] = a.getText()
                        # horses.append(a.getText())

        return horses, winner


    def loadResults(self):
        resultset = []
        readedfilecount = 0
        path = f"../datafiles/{self.location}/RaceResult/"
        files = os.listdir(path)
        files.sort()

        for filename in files:
            if filename.startswith(self.raceresultfileprefix):
                npydata = []
                npydata = np.load(path + filename, allow_pickle=True)
                # print("{}: {}".format(filename, npydata.shape))
                if npydata is not None or len(npydata) > 0:
                    resultset.extend(npydata, )

                readedfilecount = readedfilecount + 1

        resultset = np.array(resultset)
        print("read file: {0}".format(readedfilecount))
        return resultset

    def loadCards(self):
        card = []
        readfilecount = 0
        path = f"../datafiles/{self.location}/RaceCard/"
        files = os.listdir(path)
        files.sort()

        for filename in files:
            if filename.startswith(self.racecardfileprefix):
                npydata = []
                npydata = np.load(path + filename, allow_pickle=True)
                # print("{}: {}".format(filename, npydata.shape))
                if npydata is not None or len(npydata) > 0:
                    card.extend(npydata, )

                readfilecount = readfilecount + 1

        print("read file: {0}".format(readfilecount))
        if card is not None and len(card) > 0:
            card = np.array(card)

        return card

    def loadHorses(self):
        horses = []
        readfilecount = 0
        path = f"../datafiles/{self.location}/"
        files = os.listdir(path)
        files.sort()

        for filename in files:
            if filename.startswith(self.racehorsefileprefix):
                npydata = []
                npydata = np.load(path + filename, allow_pickle=True)
                # print("{}: {}".format(filename, npydata.shape))
                if npydata is not None or len(npydata) > 0:
                    horses.extend(npydata, )

                readfilecount = readfilecount + 1
                print("read file: {0}".format(filename))

        if horses is not None and len(horses) > 0:
            horses = np.array(horses)

        return horses
