
from abc import ABC
import keras
import numpy
import os
import pandas
from tensorflow.python.keras.layers.core import Dense, Dropout
from tensorflow.python.keras.layers.recurrent import LSTM


os.environ["CUDA_VISIBLE_DEVICES"] = "0"


data = pandas.read_excel("Good predict.xlsx", sheet_name=None)
states = list(data)


def get_related_size(array: type(list)):
    min_num = array[0]
    max_num = array[0]
    for n in array:
        if min_num > n:
            min_num = n
        if max_num < n:
            max_num = n
    d = max_num - min_num
    result = numpy.zeros((len(array)))
    for iterator in range(len(array)):
        result[iterator] = (array[iterator] - min_num) / d
    return result, d, min_num


def anti_related_size(array: type(list), diff: type(int), min_number: type(int)):
    result = numpy.zeros((len(array)))
    for iterator in range(len(array)):
        result[iterator] = array[iterator] * diff + min_number
    return result


class MyLSTMSequential(keras.Model):
    def __init__(self):
        super(MyLSTMSequential, self).__init__()
        self.layer_array = [LSTM(units=100, return_sequences=True, activation='relu'),
                            LSTM(units=100, activation='relu'),
                            Dense(units=1)]

    def call(self, inputs, training=None, mask=None):
        result = inputs
        for layer in self.layer_array:
            result = layer(result)
        return result

    def __repr__(self):
        name = '{}_Model'.format(self.model_name)
        return name


for state in states:
    model = MyLSTMSequential()
    model.compile(optimizer="adam", loss="mae")

    x_data = []
    y_data = []
    source_data = get_related_size(data[state][1])[0]
    for i in range(len(source_data)-10):
        x_data.append(source_data[i:i+5])
        y_data.append((source_data[i+5],))

    x_train = numpy.array(x_data)
    y_train = numpy.array(y_data)
    x_train = numpy.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    x_test = []
    y_test = []
    for i in range(len(source_data)-10, len(source_data)-5):
        x_test.append(source_data[i:i+5])
        y_test.append((source_data[i+5],))
    x_test = numpy.array(x_test)
    y_test = numpy.array(y_test)
    x_test = numpy.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))

    print("--------------")
    print("x:")
    print(x_data)
    print("--------------")
    print("y:")
    print(y_data)
    print("--------------")

    print("----start training----")
    model.fit(x=x_train, y=y_train, epochs=2000, batch_size=7, validation_data=(x_test, y_test))

    print("----stop training-----")
    print(model.summary())

    model.save("good model pro/" + state + ".tf", save_format="tf")
