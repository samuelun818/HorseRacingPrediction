import os
import numpy as np

datapath = "./DataFiles/"


def save_datafile(filename, data):
    if len(data) > 0:
        np.save('{0}{1}'.format(datapath, filename), data)
        print(f'Saved data({len(data)}) in {filename}')

def load_datafile(filename):
    data = np.load("{0}{1}".format(datapath, filename), allow_pickle=True)
    return data

def load_fileset(path, fileSeriesName):
    dataset = []
    readedfilecount = 0

    files = os.listdir(path)
    files.sort()

    for filename in files:
        if filename.startswith(fileSeriesName):
            npydata = []
            npydata = load_datafile(filename)
            if npydata is not None or len(npydata) > 0:
                dataset.extend(npydata, )

            readedfilecount = readedfilecount + 1

    dataset = np.array(dataset)
    print("read file: {0}".format(readedfilecount))
    return dataset


def delete(filename):
    return

def move(filepath, targetpath):
    return

def copy(filepath, targetpath):
    return


def exists(path):
    result = False
    if os.path.exists(path):
        result = True

    return result