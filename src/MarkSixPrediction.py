import os
import sys
import numpy as np

import argparse

from sklearn.model_selection import train_test_split

import keras
from keras import Sequential
from keras.layers import Dense, Input, LSTM, Dropout


def Load_Lotteries():
    dataset = []
    readedfilecount = 0
    path = "../DataFiles/MarkSix/"
    files = os.listdir(path)
    files.sort()

    for filename in files:
        if filename.startswith("HK_Lotteries"):
            npydata = []
            npydata = np.load(path + filename, allow_pickle=True)
            # print("{}: {}".format(filename, npydata.shape))
            if npydata is not None or len(npydata) > 0:
                dataset.extend(npydata, )

            readedfilecount = readedfilecount + 1

    dataset = np.array(dataset)
    print("read file: {0}".format(readedfilecount))
    return dataset

def transform_Lotteries(lotteries):
    outputsize = 49
    # x = np.zeros((lotteries.shape[0], outputsize), dtype="float")
    # y = np.zeros((lotteries.shape[0], outputsize), dtype="float")

    x = np.zeros((lotteries.shape[0], 1, outputsize), dtype="float")
    y = np.zeros((lotteries.shape[0], outputsize), dtype="float")

    for i in range(len(lotteries)):
        balls = lotteries[i]['balls']

        x[i][0] = np.sum(y[:i], axis=0)
        for b in balls:
            y[i][b - 1] = 1

    print(x[100], y[100])
    return x, y

def model_train(X_train, y_train):
    n_features = X_train.shape[1]
    n_class = y_train.shape[1]
    n_nodes = round(n_class / 10)

    print("Input features: {input}; Output classes: {output}; Training nodes: {nodes}".format(input=n_features,
                                                                                              output=n_class,
                                                                                              nodes=n_nodes))
    print("Input features: {input}; Output classes: {output}".format(input=n_features, output=n_class))
    # model = Sequential()
    model = Sequential(
        [
            Input(shape=(n_features, n_class)),
            # Bidirectional(LSTM(n_nodes, return_sequences=True)),
            LSTM(64, recurrent_dropout=0.1, return_sequences=True),
            # Dropout(0.2),
            LSTM(128, recurrent_dropout=0.1, return_sequences=True),
            LSTM(128, recurrent_dropout=0.1, return_sequences=True),
            # Dropout(0.2),
            LSTM(64, recurrent_dropout=0.1),
            Dense(n_class, activation="softmax"),
        ]
    )


    # # input layer and first hidden layer, n_features = input_nodes, hidden layer with 10 nodes
    # model.add(Input(shape=(n_features,)))
    # model.add(Dense(32, activation='tanh', kernel_initializer='he_normal'))
    # model.add(Dropout(0.2)),
    # model.add(Dense(32, activation='tanh', kernel_initializer='he_normal'))
    # model.add(Dropout(0.2)),
    # # self.model.add(Dense(2048, activation='relu', kernel_initializer='he_normal'))
    # # self.model.add(Dense(512, activation='relu', kernel_initializer='he_normal') )
    # # self.model.add(Dense(128, activation='relu', kernel_initializer='he_normal') return_sequences=True)
    # model.add(Dense(n_class, activation="softmax"))
    print("Set model")

    model.compile(optimizer="RMSprop", loss='categorical_crossentropy', metrics=['accuracy'])
    print("Compiled model")

    output = model_fit(model, X_train, y_train, 30)
    return output

def model_fit(model, x_train, y_train, epochs=30, batch=400, validation_split=0.1):
    # fit the model
    # print(batch)
    history = model.fit(x_train, y_train, epochs=epochs,  # batch_size=batch,
                                  verbose=2, validation_split=validation_split)
    print("fit model")
    print(model.summary())

    modelfile = "./Models/{}_model_{}.keras".format("maxsix", "lstm")
    model.save(modelfile)
    print("save file: ", modelfile)

    return model

def result_evaluate(model, x_test, y_test):
    loss, accuracy = model.evaluate(x_test, y_test, verbose=0)
    print("Testing loss : {loss}; accuracy: {acc}".format(loss=loss, acc=accuracy))

def predict(X):
    print(X.shape)
    X = X.reshape(1, 1, 49)
    modelfile = "./Models/{}_model_{}.keras".format("maxsix", "lstm")
    model = keras.models.load_model(modelfile)
    model.summary()

    result = model.predict(X)
    print(result.shape)

    np.savetxt('../Log/marksix_result.txt', result[0], delimiter=',')

    return

def main(args):
    lotteries = Load_Lotteries()
    print(len(lotteries))
    if args.action == "train":
        for i in range(10):
            print(i, lotteries[i])

        x, y = transform_Lotteries(lotteries)
        x = x[100:-2]
        y = y[100:-2]
        print(x.shape, y.shape)
        print(x[-1], y[-1])
        X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.2)

        model = model_train(X_train, y_train)
        result_evaluate(model, X_test, y_test)

        return
    if args.action == "predict":
        print(lotteries[-1])
        x, y = transform_Lotteries(lotteries)

        print(x[len(x) -1], y[len(y) -1])
        predict(x[len(x) -1])
        return

    # if (args.modeltype=="dense"):
    #     trainer = dense_trainer()
    # elif (args.modeltype == "lstm"):
    #     trainer = lstm_trainer()
    # else:
    #     print("incorrect model type: ", args.modeltype)
    #     return

if __name__ =="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('action', type=str)
    parser.add_argument('modeltype', type=str)
    #　parser.add_argument('location', type=str, default='HK', required=False)
    args = parser.parse_args()

    main(args)
