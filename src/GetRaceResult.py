import requests
import numpy as np
from dateutil import rrule
from datetime import datetime, date
from datetime import timedelta

import argparse

from Objects.UKRaces import *
from Objects.HKRaces import *

from Helpers import FileHelper as fh


def get_dates(startdate, enddate):
    # Get current date and time
    current_date = datetime.now()
    yesterday = current_date + timedelta(-14)
    date_string = yesterday.strftime('%Y%m%d')
    if enddate > date_string:
        enddate = date_string

    dates = []
    for dt in rrule.rrule(rrule.DAILY, \
        dtstart=datetime.strptime(startdate, '%Y%m%d'), \
        until=datetime.strptime(enddate, '%Y%m%d')):

        dates.append(dt.strftime('%Y/%m/%d'))

    return dates

def main(args):
    year = datetime.today().year
    country = args.country
    
    if args.year is None or args.year < 2000 or args.year > datetime.today().year:
        print('Incorrect year (2000-now): {}'.format(args.year))
        return
    year = args.year
    dates = get_dates('{}0101'.format(year), '{}1231'.format(year+1))

    race = None
    if (country == "HK"):
        race = HKRaces()
    elif (country == "UK"):
        race = UKRaces()
    else:
        print("Incorrect Country input.")
        return

    Races = []
    for date in dates:
        results = race.getResults(date)

        if len(results) > 0:
            Races.extend(results)
            print(f"{len(Races)} races are found before {date}.")

    if len(Races) > 0:
        fileName = "/{1}/RaceResult/RaceResult_{0}.npy".format(str(year).replace("/", ""), "HK")
        fh.save_datafile(fileName, Races)


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('country', type=str, help='Country (HK / UK)')
    parser.add_argument('year', type=int, help='Year (yyyy)')
    args = parser.parse_args()

    main(args)




