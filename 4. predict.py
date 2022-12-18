
import os
import keras.models
import matplotlib.pyplot as plt
import pandas
import numpy


def get_related_size(array: type(list)):
    min_number = array[0]
    max_num = array[0]
    for n in array:
        if min_number > n:
            min_number = n
        if max_num < n:
            max_num = n
    d = max_num - min_number
    res = []
    for iterator in range(len(array)):
        res.append((array[iterator] - min_number) / d)
    return res, d, min_number


def get_inverse_related_size(array: type(list)):
    min_number = array[0]
    max_num = array[0]
    for n in array:
        if min_number > n:
            min_number = n
        if max_num < n:
            max_num = n
    d = max_num - min_number
    res = []
    for iterator in range(len(array)):
        res.append((max_num-array[iterator]) / d)
    return res, d, max_num


def anti_related_size(array: type(list), different: type(int), min_number: type(int)):
    res = []
    for iterator in range(len(array)):
        res.append(array[iterator] * different + min_number)
    return res


def anti_inverse_size(array: type(list), different: type(int), max_number: type(int)):
    res = []
    for iterator in range(len(array)):
        res.append(0-(array[iterator] * different - max_number))


class Show:
    def __init__(self, table_path):
        self.data = pandas.read_excel(table_path, sheet_name=None)

    def show_model(self, my_model, table_name):
        source_data, diff, min_num = get_related_size(self.data[table_name][1])

        x_data = []
        for i in range(len(source_data) - 5):
            x_data.append(source_data[i:i + 5])

        x_data = numpy.array(x_data)
        x_data = numpy.reshape(x_data, (x_data.shape[0], x_data.shape[1], 1))

        y_pre = my_model.predict(x_data)

        y_pre = anti_related_size(y_pre, diff, min_num)

        actual_data = anti_related_size(source_data[5:], diff, min_num)

        loss = 0
        for i in range(len(y_pre)):
            loss += abs(y_pre[i]-actual_data[i])
        loss /= max(y_pre)

        plt.scatter(range(len(actual_data)), actual_data)

        plt.plot(range(len(actual_data)), actual_data, 'b-', lw=1)

        plt.plot(range(len(y_pre)), y_pre, 'r-', lw=1)

        plt.title("Honeybee Colony Size Change Over Time in " + table_name + "\n")

        plt.savefig("./pic/" + table_name + ".svg", format="svg", dpi=500)

        plt.show()


def get_last_five(array):
    return array[len(array)-5:]

"""
files = os.listdir("./good model pro/")
print(files)
show = Show("Good predict.xlsx")
for f in files:
    model = keras.models.load_model("./good model pro/" + f)
    print(f)
    show.show_model(model, f.replace(".tf", ""))

"""
_data = pandas.read_excel("Good predict.xlsx", sheet_name=None)
for state in list(_data):
    data = _data[state][1]
    LSTM_model = keras.models.load_model("./good model pro/" + state + ".tf")

    result = []
    for i in data:
        result.append(i)
    result, diff, min_num = get_related_size(result)

    predict_source = result[24:]
    predict_source = numpy.reshape(predict_source, (1, len(predict_source), 1))

    print(predict_source)
    for i in range(20):
        Y = LSTM_model.predict(predict_source)
        result.append(Y[0][0])
        predict_source = result[len(result)-5:]
        predict_source = numpy.reshape(predict_source, (1, len(predict_source), 1))

    result = anti_related_size(result, diff, min_num)
    result_percent = []

    for i in range(27, len(result)):
        result_percent.append((result[i] - result[27])/result[27])

    frame = pandas.DataFrame(numpy.zeros((len(result_percent), 2)))
    frame[1] = result_percent

    # with pandas.ExcelWriter("Q3_data_pro.xlsx") as writer:
    #     frame.to_excel(writer)

    plt.scatter(range(len(result)), result)
    plt.plot(range(len(data)), data, 'r-', lw=1)
    plt.plot(range(28, len(result)), result[28:], 'b-', lw=1)
    plt.title("Honeybee Colony Size Change Over Time in " + state + "\n")
    plt.savefig("./forecast_pic/" + state + ".svg", format="svg", dpi=500)
    plt.show()
