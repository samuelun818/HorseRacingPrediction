import numpy as np

import keras
from keras import Sequential
from keras.layers import Dense, Input, LSTM, Dropout, Bidirectional

import matplotlib.pyplot as pyplot


class lstm_trainer:
    def __init__(self):
        self.modeltype = "lstm"
        self.model =  None
        self.history, self.loss, self.accuracy = None, None, None
        self.ranktype = "win"
        self.le = None
        self.modelfile = "./Models/{}_model_{}.keras".format(self.ranktype, self.modeltype)
        self.result = None
        return

    def data_transform(self, racehorses, winners, bagsize):
        #　math.ceil(value)
        outputsize = 11000
        x = np.zeros((racehorses.shape[0], 16, outputsize), dtype="bool")
        y = np.zeros((winners.shape[0], outputsize), dtype="bool")

        # w = self.le.transform(winners)
        print(racehorses[0], winners[0])

        for i in range(len(racehorses)):
            y[i][winners[i]] = True

            horses = racehorses[i]  # self.le.transform(racehorses[i])
            for h in range(len(horses)):
                if racehorses[i][h] == 0:
                    continue

                x[i][h][horses[h]] = True

        np.savetxt('../logs/race_horses.txt', x[0][0], delimiter=',')
        np.savetxt('../logs/win_horses.txt', y[0], delimiter=',')
        return x, y

    def model_train(self, x_train, y_train):
        n_features = x_train.shape[1]
        n_class = y_train.shape[1]
        n_nodes = round(n_class / 10)

        print("Input features: {input}; Output classes: {output}; Training nodes: {nodes}".format(input=n_features,
                                                                                                  output=n_class,
                                                                                                  nodes=n_nodes))

        self.model = Sequential(
             [
                Input(shape=(n_features, n_class)),
                # Bidirectional(LSTM(n_nodes, return_sequences=True)),
                LSTM(n_nodes,  recurrent_dropout=0.2,  return_sequences=True),
                # Dropout(0.2),
                # LSTM(n_nodes, recurrent_dropout=0.2, return_sequences=True),
                # Dropout(0.2),
                LSTM(n_nodes,  recurrent_dropout=0.2),
                Dense(n_class, activation="softmax"),
             ]
        )

        optimizer = keras.optimizers.RMSprop(learning_rate=0.01)
        print("Set model")
        # compile the layers to model
        
        self.model.compile(optimizer=optimizer, loss='categorical_crossentropy', metrics=['accuracy'])
        print("Compile model")
        
        # fit the model
        # python 3.9 loss doesn't go down after 15
        # python 3.13

        # --- epoches 30, val_accuracy go up to 0.8
        # --- epoches 15, val_accuracy keep at 0.01
        self.fit(x_train, y_train, 40)

    def fit(self, x_train, y_train, epochs=30, batch=400, validation_split=0.1):
# fit the model
        # print(batch)
        self.history = self.model.fit(x_train, y_train, epochs=epochs, # batch_size=batch,
                                      verbose=2, validation_split=validation_split)
        print("fit model")
        print(self.model.summary())
        
        self.model.save(self.modelfile)
        print("save file: ", self.modelfile)

    def result_evaluate(self, x_test, y_test):
        self.loss, self.accuracy = self.model.evaluate(x_test, y_test, verbose=0)

    def predict(self, x):
        x = np.array(x)
        print("predict :", x.shape)

        if len(x) <= 0:
            print('Racing horses should be greater than 0.')

        if self.model is None or len(self.model.layers) <= 0:
            print(f'load model: {self.modelfile}')
            self.model = keras.models.load_model(self.modelfile)
            self.model.summary()

        # feature_dim = model.input_shape[1]
        # self.model = keras.models.load_model(self.modelfile)

        self.result = self.model.predict(x) 
        np.savetxt('./logs/race_result.txt', self.result[0], delimiter=',')
        return self.result

    def plot_history(self):
        if self.history is None:
            return
        
        filename = "plot_RacingPredictionTraining_{}.png".format(self.modeltype.upper())
        # plot loss during training
        pyplot.subplot(211)
        pyplot.title('Loss / Categorical Cross Entropy ({})'.format(self.modeltype.upper()))
        pyplot.plot(self.history.history['loss'], label='train')
        pyplot.plot(self.history.history['val_loss'], label='test')
        # plot accuracy during training
        pyplot.subplot(212)
        pyplot.title('Accuracy')
        pyplot.plot(self.history.history['accuracy'], label='train')
        pyplot.plot(self.history.history['val_accuracy'], label='test')
        pyplot.legend()
        pyplot.savefig(filename)

    def plot_result(self, out):
        if self.result is None:
            return
        
        filename = "plot_RacingPredictionResult_{}.png".format(self.modeltype.upper())
        # plot original value
        # pyplot.subplot(311)
        # pyplot.title('Original')
        # pyplot.plot(y, label='original_y')
        # pyplot.legend()
        # plot all prediction value
        pyplot.subplot(312)
        pyplot.title('Prediction')
        pyplot.plot(self.result, label='prediction_y')
        pyplot.legend()
        # plot predict race value
        pyplot.subplot(313)
        pyplot.title('Prediction racing horses')
        pyplot.plot(out, label='prediction racing')
        pyplot.legend()
        pyplot.savefig(filename)
        
