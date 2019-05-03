# -*- coding: utf-8 -*-

import time
import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.layers.core import Dense, Activation, Dropout
from keras.layers.recurrent import LSTM
from keras.models import Sequential
from model_evaluation import model_evaluation
from keras import backend as K
import tensorflow as tf

class Conf:
    # epochs
    EPOCHS = 10
    SEQ_LEN = 50
    PREDICT_STEP = 10
    TRAIN_DATA_RATE = 0.8
    BATCH_SIZE = 64
    LAYERS = [1, 50, 100, 1]
    window0=0


def normalise_windows(window_data):
    normalised_data = []
    for window in window_data:
        normalised_window = [((float(p) / float(window[0])) - 1) for p in window]
        Conf.window0=float(window[0])
        normalised_data.append(normalised_window)
    return normalised_data


def load_data(filepath):
    data = pd.read_csv(filepath,usecols=[4]).values
    result = []
    for index in range(len(data) - Conf.SEQ_LEN - 1):
        result.append(data[index: index + Conf.SEQ_LEN + 1])
    result = normalise_windows(result)
    result = np.array(result)
    row = round(result.shape[0] * Conf.TRAIN_DATA_RATE)
    train = result[:int(row), :]
    np.random.shuffle(train)

    _X_train = train[:, :-1]
    _y_train = train[:, -1]
    _X_test = result[int(row):, :-1]
    _y_test = result[int(row):, -1]
    _X_train = _X_train[:, :, np.newaxis]
    _X_test = _X_test[:, :, np.newaxis]
    return [_X_train, _y_train, _X_test, _y_test]


def build_model(layers):

    model = Sequential()

    model.add(LSTM(units=layers[1], input_shape=(layers[1], layers[0]), return_sequences=True))
    model.add(Dropout(0.5))

    model.add(LSTM(layers[2], return_sequences=False))
    model.add(Dropout(0.5))

    model.add(Dense(units=layers[3]))
    model.add(Activation("tanh"))

    start = time.time()
    model.compile(loss="mse", optimizer="Adam")
    print("> Compilation Time : ", time.time() - start)
    return model


def predict_point_by_point(model, data, path):
    model.load_weights(path)
    predict = model.predict(data)
    predict = np.reshape(predict, (len(predict),))
    return predict


def predict_point_by_point_short(model, data, path):
    model.load_weights(path)
    predict = model.predict(data)
    predict_const = predict
    predict_const = np.reshape(predict_const, (len(predict_const),))

    predict = predict[:, :, np.newaxis]
    new_data = np.concatenate((data, predict), axis=1)
    new_data = new_data[:, 1:, :]
    predict = model.predict(new_data)
    for i in range(9):
        predict = predict[:, :, np.newaxis]
        new_data = np.concatenate((new_data,predict), axis=1)
        new_data = new_data[:,1:,:]
        predict = model.predict(new_data)

    predict = np.reshape(predict, (len(predict),))
    predict_new = predict[-10:]
    predict = np.concatenate((predict_const, predict_new), axis = 0)
    return predict


def predict_point_by_point_long(model, data, path):
    model.load_weights(path)
    predict = model.predict(data)
    predict_const = predict
    predict_const = np.reshape(predict_const, (len(predict_const),))
    predict = predict[:, :, np.newaxis]
    new_data = np.concatenate((data, predict), axis=1)
    new_data = new_data[:, 1:, :]
    predict = model.predict(new_data)
    for i in range(49):
        predict = predict[:, :, np.newaxis]
        new_data = np.concatenate((new_data, predict), axis=1)
        new_data = new_data[:, 1:, :]
        predict = model.predict(new_data)

    predict = np.reshape(predict, (len(predict),))
    predict_new = predict[-50:]
    predict = np.concatenate((predict_const, predict_new), axis=0)
    return predict

def plot_results(y_true, y_pred, filename):
    fig = plt.figure(facecolor='white')
    ax = fig.add_subplot(111)
    ax.plot((1+y_true)*Conf.window0, label='True Price')
    plt.plot((1+y_pred)*Conf.window0, label='Predicted Price')
    plt.legend()
    #plt.show()
    fig.savefig('static/images/lstm_fig.png')


def go(filename, function_type, term):
    filepath='dataset/{}.csv'.format(filename)
    global_start_time = time.time()
    X_train, y_train, X_test, y_test = load_data(filepath)
    print('> Loading data... ')
    print('> Data Loaded. Compiling...')
    ###
    warmup = np.zeros([1, 50])
    warmup = warmup[:,:, np.newaxis]
    global graph
    ###
    if function_type == 'train':
        if not os.path.exists('static/images/'):
            os.makedirs('static/images/')

        model = build_model(Conf.LAYERS)
        ###
        model.predict(warmup)
        ###
        if not os.path.exists('weights/'+filename + '_saved/'):
            saved_model_path = 'weights/'+filename + '_saved/'
            os.makedirs('weights/'+filename + '_saved/')
        else:
            saved_model_path = 'weights/'+filename + '_saved/'
        model.fit(X_train, y_train, batch_size=Conf.BATCH_SIZE, epochs=Conf.EPOCHS, validation_split=0.05)
        model.save_weights(saved_model_path + '_saved_weights.h5')
        ###
        model._make_predict_function()
        session = K.get_session()
        graph = tf.get_default_graph()
        ###
        predicted = predict_point_by_point(model, X_test,saved_model_path+'_saved_weights.h5')
        print('Training duration (s) : ', time.time() - global_start_time)
        plot_results(y_test, predicted, filename)
        model_evaluation(pd.DataFrame(y_test), pd.DataFrame(predicted))
        #exit()

    if function_type == 'test':
        saved_model_path = 'weights/'+filename + '_saved/'
        model = build_model(Conf.LAYERS)
        ###
        model.predict(warmup)
        ###
        ###
        model._make_predict_function()
        session = K.get_session()
        graph = tf.get_default_graph()
        ###
        if term == 'SHORT':
            predicted = predict_point_by_point_short(model, X_test, saved_model_path + '_saved_weights.h5')
            print('short_term shape:', predicted.shape)
        elif term == 'LONG':
            predicted = predict_point_by_point_long(model, X_test, saved_model_path + '_saved_weights.h5')
            print('long_term shape:',predicted.shape)
        pred = predicted[y_test.shape[0]:predicted.shape[0]]
        pred = (1 + pred) * Conf.window0
        plot_results(y_test, predicted, filename)
        return pred
        #exit()


#print(go('amzn', 'test', 'SHORT'))

