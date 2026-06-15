from Objects.HKRaces import *
from Objects.UKRaces import *
from Helpers import FileHelper as fh

import argparse


def main(args):
    country = args.country

    race = None
    if (country == "HK"):
        race = HKRaces()
    elif (country == "UK"):
        race = UKRaces()
    else:
        print("Incorrect Country input.")
        return

    Horses = race.getHorses()
    if len(Horses) > 0:
        fileName = ("{0}\RaceHorse.npy").format( country)
        fh.save_datafile(fileName, Horses)

        print(f'{len(Horses)} horses save in {fileName}')
    return

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('country', type=str, help='Country (HK / UK)')
    # parser.add_argument('racedate', type=str)
    args = parser.parse_args()
    main(args)
