import numpy as np

import keras
from keras import Sequential
from keras.layers import Dense, Input, LSTM, Dropout

import matplotlib.pyplot as pyplot


class dense_trainer:
    def __init__(self):
        self.model= None
        self.modeltype = 'dense'
        self.history, self.loss, self.accuracy = None, None, None
        self.result = None
        self.ranktype = 'win'
        
        self.le = None
        self.modelfile = "./Models/{}_model_{}.keras".format(self.ranktype, self.modeltype);
        return

    def data_transform(self, racehorses, winners, bagsize):
        x = np.zeros((racehorses.shape[0], bagsize), dtype="float")
        y = np.zeros((winners.shape[0], bagsize), dtype="float")

        # w = self.le.transform(winners)
        # c = collections.Counter(w)      

        for i in range(len(racehorses)):
            y[i][winners[i]] = 1
            
            pre_winners = winners[:i-1]
            pre_races = racehorses[:i-1]
            # print("{} pre_races: {} ".format(i, len(pre_races)))
            horses = racehorses[i] # self.le.transform(racehorses[i]) 
            for h in range(len(horses)):
                if racehorses[i][h] == 0:
                    continue

                score = []
                previous = np.argwhere(pre_races == racehorses[i][h])
                if previous.size > 0:
                    score = (1 - (previous[:, 1] / 120))
                    # score = 1- (score / 16)
                    
                score = np.append(score, 1/16) 
                ind = [((i + 1) / len(score)) * val    for i, val in enumerate(score)]
                    #score = np.array(score, dtype=float)
                    # print(racehorses[i][h],  sum(ind))
                x[i][horses[h]] = np.round( sum(ind),3 )

        if x.shape[0] > 100:
            x = x[100:]
            y = y[100:]
            np.savetxt('./Log/race_horses.txt', x[0], delimiter=',')
            np.savetxt('./Log/win_horses.txt', y[0], delimiter=',')

        return x, y
    
    
    def model_train(self, x_train, y_train):
        n_features = x_train.shape[1]
        n_class = y_train.shape[1]
        n_nodes = round(n_class / 10)

        print("Input features: {input}; Output classes: {output}; Training nodes: {nodes}".format(input=n_features,
                                                                                                  output=n_class,
                                                                                                  nodes=n_nodes))

        self.model = Sequential()
        print("Input features: {input}; Output classes: {output}".format(input=n_features, output=n_class))
        # input layer and first hidden layer, n_features = input_nodes, hidden layer with 10 nodes
        self.model.add(Input(shape=(n_features, )))
        self.model.add(Dense(n_nodes, activation='tanh', kernel_initializer='he_normal'))
        self.model.add(Dropout(0.2)),
        self.model.add(Dense(n_nodes, activation='tanh', kernel_initializer='he_normal'))
        self.model.add(Dropout(0.2)),
        # self.model.add(Dense(2048, activation='relu', kernel_initializer='he_normal'))
        # self.model.add(Dense(512, activation='relu', kernel_initializer='he_normal') )
        # self.model.add(Dense(128, activation='relu', kernel_initializer='he_normal') return_sequences=True)
        self.model.add(Dense(n_class, activation="softmax"))
        print("Set model")

        self.model.compile(optimizer="RMSprop", loss='categorical_crossentropy', metrics=['accuracy'])
        print("Compiled model")

        # fit the model
        self.fit(x_train, y_train, 40)

    
    def fit(self, x_train, y_train, epochs=40, validation_split=0.1):
        # fit the model
        self.history = self.model.fit(x_train, y_train, epochs=epochs, #batch_size=32, 
                                      verbose=2, validation_split=validation_split)
        
        print("fit model")
        print(self.model.summary())
        
        self.model.save(self.modelfile)
        print("save file: ", self.modelfile)

    
    def result_evaluate(self, x_test, y_test):
        self.loss, self.accuracy = self.model.evaluate(x_test, y_test, verbose=0)

    
    def predict(self, x):
        x = np.array(x)
        print("predict", x.shape)
        
        if self.model is None or len(self.model.layers) <= 0:
            self.model = keras.models.load_model(self.modelfile)
            self.model.summary()

        self.result = self.model.predict(x) 
        np.savetxt('./Log/race_result.txt', self.result[0], delimiter=',')
        return self.result


    
    def plot_history(self):

        if self.history is None: 
            return

        filename = "plot_RacingPredictionTraining_{}.png".format(self.modeltype)
        # plot loss during training
        pyplot.subplot(211)
        pyplot.title('Loss / Categorical Cross Entropy ({})'.format(self.modeltype))
        pyplot.plot(self.history.history['loss'], label='train')
        pyplot.plot(self.history.history['val_loss'], label='test')
        # plot accuracy during training
        pyplot.subplot(212)
        pyplot.title('Accuracy')
        pyplot.plot(self.history.history['accuracy'], label='train')
        pyplot.plot(self.history.history['val_accuracy'], label='test')
        pyplot.legend()
        pyplot.savefig(filename)
        
        return

    def plot_result(self):
        if self.result is None:
            return
        
        filename = "plot_RacingPredictionResult_{}.png".format(self.modeltype)
        # plot original value
        pyplot.subplot(311)
        pyplot.title('Original')
        pyplot.plot(y, label='original_y')
        pyplot.legend()
        # plot all prediction value
        pyplot.subplot(312)
        pyplot.title('Prediction')
        pyplot.plot(pred_y, label='prediction_y')
        pyplot.legend()
        # plot predict race value
        pyplot.subplot(313)
        pyplot.title('Prediction racing horses')
        pyplot.plot(out, label='prediction racing')
        pyplot.legend()
        pyplot.savefig(filename)
        
        return
        