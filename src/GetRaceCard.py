
from datetime import datetime

import argparse

from Crawlers.HKRaces import *
from Crawlers.UKRaces import *
from Helpers import FileHelper as fh

def main(args):
    racedate = args.racedate # '20260107'
    date = datetime.strptime(racedate, '%Y%m%d')
    country = args.country # "HK"

    race = None
    if (country=="HK"):
        race = HKRaces()
    elif (country=="UK"):
        race = UKRaces()
    else:
        print("Incorrect Country input.")
        return

    Races = race.getCards(date)

    if len(Races) > 0:
        fileName = ("{1}\RaceCard\RaceCard_{0}.npy").format(racedate, country)
        fh.save_datafile(fileName, Races)

    return

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('country', type=str, help='Country (HK / UK)')
    parser.add_argument('racedate', type=str, help='Race Date (yyyymmdd)')
    args = parser.parse_args()
    main(args)
