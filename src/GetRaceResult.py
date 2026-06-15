import requests
import numpy as np
from dateutil import rrule
from datetime import datetime, date
from datetime import timedelta

import argparse

from bs4 import BeautifulSoup
from Objects.HKRaces import *

from Helpers import FileHelper as fh


def getraceresult(date,venue,no):
    
    url = "https://racing.hkjc.com/racing/information/English/Racing/LocalResults.aspx?RaceDate={}&Racecourse={}&RaceNo={}".format(
        date, venue, no)
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWeKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}

    # Send an HTTP GET request to the website
    response = requests.get(url, headers=headers)

    # Parse the HTML code using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    # print(soup)
    stocks = {}

    horses = []
    win = ''
    div = soup.find_all('div', {'class': "performance"})
    if len(div) <= 0:
        return None

    divcounter = 0
    for d in div:
        if divcounter >= 1:
            break

        # print(d)
        rows = d.select('tr')
        divcounter = divcounter + 1
        rowcounter = 0
        for row in rows:

            trsoup = BeautifulSoup(str(row), 'html.parser')
            links = trsoup.find_all('a', {'class': "local"})
            for a in links:
                if 'HorseId' in a['href']:

                    if rowcounter == 1 :
                         win = a.getText()
                    
                    horses.append(a.getText())
                    
            rowcounter = rowcounter + 1

    race = {}
    race['date'] = date
    race['venue'] = venue
    race['race_no'] = no
    race['horses'] = horses
    race['win'] = win

    return race

def get_dates(startdate, enddate):
    dates = []

    # Get current date and time
    current_date = datetime.now()
    yesterday = current_date + timedelta(-14)
    date_string = yesterday.strftime('%Y%m%d') # Example format: '2023-10-05'
    if enddate > date_string:
        enddate = date_string 
    
    for dt in rrule.rrule(rrule.DAILY, \
        dtstart=datetime.strptime(startdate, '%Y%m%d'), \
        until=datetime.strptime(enddate, '%Y%m%d')):

        dates.append(dt.strftime('%Y/%m/%d'))

    return dates

def main(args):
    year = datetime.today().year
    
    if args.year is None or args.year < 2000 or args.year > datetime.today().year:
        print('Incorrect year (2000-now): {}'.format(args.year))
        return
    year = args.year
    
    startdate = '{}0101'.format(year)
    enddate = '{}1231'.format(year+1)
    dates = get_dates(startdate, enddate)
    Races = []

    ##
    for date in dates:
        # print("Download Races Result: {0}".format(date))

        races = HKRaces()
        results = races.getResults(date)

        if len(results) > 0:
            Races.extend(results)
            print(f"{len(Races)} races are found before {date}.")

    if len(Races) > 0:
        fileName = "/RaceResult/{1}_RaceResult_{0}.npy".format(str(year).replace("/", ""), "HK")
        fh.save_datafile(fileName, Races)



if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int)
    args = parser.parse_args()

    main(args)




