
import requests
import numpy as np
from datetime import datetime

from Objects.HKRaces import *
from Helpers import FileHelper as fh

import argparse

from bs4 import BeautifulSoup

def getracehorse():
    horses = []
    races = HKRaces()
    horses = races.getHorses()

    return horses

def main(args):
    Horses = getracehorse()
    fh.save_datafile('HK_RaceHorse.npy', Horses)
    # if len(Horses) > 0:
    #     np.save('./datafiles/HK_RaceHorse.npy'.format(), Horses)
    #     print(f'{len(Horses)} horses save in RaceHorse_HK.npy')
    return

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    # parser.add_argument('racedate', type=str)
    args = parser.parse_args()
    main(args)
