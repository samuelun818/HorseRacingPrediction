import requests
import numpy as np

from dateutil import rrule
from datetime import datetime, date
from datetime import timedelta

import argparse

from Helpers import FileHelper as fh
from Objects.HKMarkSix import *

def main(args):
    year = datetime.today().year

    if args.year is None or args.year < 2000 or args.year > datetime.today().year:
        print('Incorrect year (2000-now): {}'.format(args.year))
        return
    year = args.year
    lottery = HKMarkSix()
    Lotteries = []

    y = year
    for i in range(10):
        results = lottery.getLotteries(y)

        if len(results) > 0:
            print('{} lotteries are drawn in {}'.format(len(results), y))
            Lotteries.extend(results)
        else:
            break

        y = y + 1


    if len(Lotteries) > 0:
        print(Lotteries[0])
        print(Lotteries[1])
        print(Lotteries[2])

        fileName = "/MarkSix/{1}_Lotteries_{0}.npy".format(str(year).replace("/", ""), "HK")
        fh.save_datafile(fileName, Lotteries)
        print('Totally saved {} lotteries'.format(len(Lotteries)))


if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('year', type=int)
    args = parser.parse_args()

    main(args)