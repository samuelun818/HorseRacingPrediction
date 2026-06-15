
from sklearn import preprocessing
import numpy as np

class bag_of_horses:
    def __init__(self):
        self.horses = None
        self.races = []
        self.le = preprocessing.LabelEncoder()
        return

    def fill_horsebag(self, races):
        self.horses = []
        self.horses.append("")
        
        for race in races:
            horses = race["horses"]
            self.append_horses(horses)

        print ("Total horses： {numofhorses}".format(numofhorses=len(self.horses)))
        self.save_horsebag()

    def append_horsebag(self, races):
        for race in races:
            appended = self.append_horses(race["horses"])

        print ("Appended horses： {numofhorses}".format(numofhorses=len(self.horses)))
        self.save_horsebag()

    def append_horses(self, horses):
        isAppended = False
        for horse in horses:
            if horse != "" and horse not in self.horses:
                self.horses = np.append(self.horses, horse)
                isAppended = True

        self.le.fit(self.horses)
        return isAppended

    def save_horsebag(self):
        self.horses = np.array(self.horses)
        np.save('././DataFiles/bagofhorse.npy', self.horses)

    def load_horsebag(self):
        # Load the .npy file
        self.horses = np.load('././DataFiles/bagofhorse.npy')

        self.le.fit(self.horses)
        print ("Loaded horses： {numofhorses}".format(numofhorses=len(self.horses)))

    def vectorize_races(self, racedata, venue):
        if self.horses is None or len(self.horses) <=0:
            return None

        races, winners = [], []
        for race in racedata:
            # if venue != race["venue"]:
            #     continue

            horses = race["horses"]
            # horses = np.array(horses)

            if 'win' in race:
                winners.append(race["win"])
            else:
                winners.append("")

            if len(horses) < 16:
                for i in range(16 - len(horses)):
                    horses.append("")
                    
            horses = self.le.transform(horses)
            # r = self.transform_race(horses)
            races.append(horses)

        races = np.array(races)
        winners = self.le.transform(winners)
        winners = np.array(winners)
        
        return races, winners

    



