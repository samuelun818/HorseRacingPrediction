from Objects.Races import *

#　https://www.racingtv.com/results/2026-02-11
# https://www.racingtv.com/results/2026-03-04/catterick-bridge/1410

class UKRaces(Races):
    def __init__(self):
        super().__init__()
        self.racecardurl = "https://racing.hkjc.com/racing/information/English/racing/RaceCard.aspx"
        self.racecardquery="?RaceDate={}&Racecourse={}&RaceNo={}"
        self.raceresulturl = "https://www.racingtv.com/results"
        self.racereuslturl = "/{racedate}/{racevenue}/{racetime}"
        self.racehorseurl = "https://www.racingtv.com/profiles/horse"
        self.racehorsequery = "/{alphabet}?page=1"
        self.venues = ['HV', 'ST']
        self.nos = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', ]
        self.numofHorse = 10

    def getResults(self, date):
        return

    def getCards(self, date):
        return