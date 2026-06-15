import os
import sys
import numpy as np
from sklearn.model_selection import train_test_split

from Trainers.BagofHourse import bag_of_horses
from Trainers.Dense_Trainer import dense_trainer
from Trainers.LSTM_Trainer import lstm_trainer

from matplotlib import pyplot

import argparse


bag = bag_of_horses()
trainer = None

def Load_RaceResult():
    dataset = []
    readedfilecount = 0
    path = "../datafiles/HK/RaceResult/"
    files = os.listdir(path)
    files.sort()

    for filename in files:
        if filename.startswith("HK_RaceResult"):
            npydata = []
            npydata = np.load(path + filename, allow_pickle=True)
            #print("{}: {}".format(filename, npydata.shape))
            if npydata is not None or len(npydata) > 0:
                dataset.extend(npydata, )

            readedfilecount = readedfilecount + 1
    
    dataset = np.array(dataset)
    print("read file: {0}".format(readedfilecount))
    return dataset

def load_RaceHorse():
    dataset = []
    readfilecount = 0
    path = "../datafiles/"
    files = os.listdir(path)
    files.sort()

    for filename in files:
        if filename.startswith("HK_RaceHorse"):
            npydata = []
            npydata = np.load(path + filename, allow_pickle=True)
            # print("{}: {}".format(filename, npydata.shape))
            if npydata is not None or len(npydata) > 0:
                dataset.extend(npydata, )

            readfilecount = readfilecount + 1
            print("read file: {0}".format(filename))

    if dataset is not None and len(dataset) > 0:
        dataset = np.array(dataset)

    return dataset

def load_RaceCard():
    dataset = []
    readfilecount = 0
    path = "../datafiles/"
    files = os.listdir(path)
    files.sort()

    for filename in files:
        if filename.startswith("HK_RaceCard_"):
            npydata = []
            npydata = np.load(path + filename, allow_pickle=True)
            #print("{}: {}".format(filename, npydata.shape))
            if npydata is not None or len(npydata) > 0:
                dataset.extend(npydata, )

            readfilecount = readfilecount + 1

    print("read file: {0}".format(readfilecount))
    if dataset is not None and len(dataset) > 0:
        dataset = np.array(dataset)

    return dataset

def Training(trainer , race_horses, win_horses, training_size=1):
    size = round(race_horses.shape[0] - (race_horses.shape[0] * training_size))
    race_horses = race_horses[size:]
    win_horses = win_horses[size:]
    print("Training Size: {0} / {1}".format(race_horses.shape, win_horses.shape))

    x, y = trainer.data_transform(race_horses, win_horses, len(bag.horses))
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)
    print ("Split Size: {0} / {1}".format(X_train.shape, y_train.shape) )

    trainer.model_train(X_train, y_train)

    print ("Evaluating Size: {0} / {1}".format(X_test.shape, y_test.shape) )
    trainer.result_evaluate(X_test, y_test)
    print("Testing loss : {loss}; accuracy: {acc}".format(loss=trainer.loss, acc=trainer.accuracy))

    trainer.plot_history()
    return

def Prediction(trainer, next_races, next_results):

    # next_x, next_y, next_races, next_winners, isAppended = GetNextRace(race_horses, race_winner)
    # if isAppended:
    #     return False, isAppended
    next_x, next_y = trainer.data_transform(next_races, next_results, len(bag.horses))
    print ("transfromed : {0} / {1}".format(next_x.shape, next_y.shape) )
    
    win_y = []
    results = {}
    for i in range(len(next_x)):
        print("Race No {0}:".format(i+1))
        pred_y = trainer.predict([next_x[i]])
        pred = np.argmax(pred_y)
        print("Prediction max value: {0}({1}) [{2}]".format(pred, np.max(pred_y), bag.le.inverse_transform([pred])))

        pred_results = []
        
        x_idx = next_races[i]
        for j in range(len(x_idx)):
            r = {}
            r['no'] = j + 1
            r['probability'] = pred_y[0][x_idx[j]]
            r['horse'] = bag.le.inverse_transform([x_idx[j]])
            pred_results.append(r)
        
        out = pred_y[0][x_idx]
        
        print(out)
        print(x_idx)
        print(bag.le.inverse_transform(x_idx))
        results[i] = pred_results

    print(results)
    
    return True

def main(args):
    if (args.modeltype=="dense"):
        trainer = dense_trainer()
    elif (args.modeltype == "lstm"):
        trainer = lstm_trainer()
    else:
        print("incorrect model type: ", args.modeltype)
        return

    venue = "ST"
    if args.action == "train":
        raceResult = Load_RaceResult()
        print("No of race: {}".format(raceResult.shape[0]))

        bag.fill_horsebag(raceResult)
        print("Filled bag of Horses: {}".format(bag.horses.shape))

        raceHorses = load_RaceHorse()
        if (bag.append_horses(raceHorses)):
            bag.save_horsebag()
        print("Appended active horses: {}".format(bag.horses.shape))
        if "CALL ME MAGNIFIQUE" in bag.horses:
            print("CALL ME MAGNIFIQUE exist")


        race_horses, race_winners = bag.vectorize_races(raceResult, venue)
        print("Vectorize train Races ({2}): {0} / {1}".format(race_horses.shape, race_winners.shape, venue))

        Training(trainer, race_horses, race_winners)

    if args.action == "predict":
        bag.load_horsebag()   # 10762

        raceCard = load_RaceCard()
        isAppended, isCompleted = False, False

        ## predicting
        while not isCompleted:
            try:
                # if isAppended:
                #     print("Retrain Models with new horses.")
                #     race_horses, race_winners = bag.vectorize_races(raceResult)
                #     print("Vectorize train Races: {0} / {1}".format(race_horses.shape, race_winners.shape))
                #
                #     Training(trainer, race_horses, race_winners)
                #     isAppended = False
                #     print("Retrained. ({})".format(isAppended))
                print(venue)
                next_horses, next_results = bag.vectorize_races(raceCard, venue)
                print ("Vectorize new races: {0} / {1}".format(next_horses.shape, next_results.shape))

                isCompleted = Prediction(trainer, next_horses, next_results)
            except Exception as e:
                if "unseen labels" in str(e):
                    print(f"New horse exists. {e}")
                    # isAppended = True
                    # bag.append_horsebag(raceCard)
                    isCompleted = True
                else:
                    print(f"Exception occurred: {e}")
                    isCompleted = True

    
if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', type=str)
    parser.add_argument('modeltype', type=str)
    #　parser.add_argument('location', type=str, default='HK', required=False)
    args = parser.parse_args()

    main(args)





