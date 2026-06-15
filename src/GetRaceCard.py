## https://racing.hkjc.com/racing/information/English/racing/RaceCard.aspx?RaceDate=2026/01/04&Racecourse=ST&RaceNo=2
import requests
import numpy as np
from datetime import datetime

import argparse

from bs4 import BeautifulSoup

from Objects.HKRaces import *
from Objects.UKRaces import *
from Helpers import FileHelper as fh

def main(args):
    racedate = args.racedate # '20260107'
    date=datetime.strptime(racedate, '%Y%m%d')
    country = "HK"

    races = None
    if (country=="HK"):
        races = HKRaces()
    elif (country=="UK"):
        races = UKRaces()
    else:
        print("Incorrect Country input.")
        return

    Races = races.getCards(date)

    if len(Races) > 0:
        fileName = "{1}_RaceCard_{0}.npy".format(racedate, country)
        fh.save_datafile(fileName, Races)

    return

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('racedate', type=str)
    args = parser.parse_args()
    main(args)
