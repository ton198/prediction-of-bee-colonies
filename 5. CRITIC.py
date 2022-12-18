import pandas


def get_related_size(array):
    min_num = array[0]
    max_num = array[0]
    for n in array:
        if min_num > n:
            min_num = n
        if max_num < n:
            max_num = n
    d = max_num - min_num
    result = []
    for iterator in range(len(array)):
        result.append((array[iterator] - min_num) / d)
    return result, d, min_num


def get_average(array):
    total = 0
    for item in array:
        total += item
    return total/len(array)


def get_temperate_difference(array1, array2):
    result = []
    for iterator in range(len(array1)):
        diff1 = abs(array1[iterator] - 22.5)
        if diff1 < 2.5:
            diff1 = 0
        diff2 = abs(array2[iterator] - 22.5)
        if diff2 < 2.5:
            diff2 = 0
        diff = diff1 + diff2
        result.append(diff)
    return result


def get_standard_difference(array):
    average = get_average(array)
    standard_difference_p = 0
    column_length = len(array)
    for item in array:
        standard_difference_p += (((item - average) ** 2) / (column_length - 1)) ** 0.5
    return standard_difference_p


def get_r(array1, array2):
    average_1 = get_average(array1)
    average_2 = get_average(array2)
    numerator = 0
    denominator_x = 0
    denominator_y = 0
    for iterator in range(len(array1)):
        xi_xa = array1[iterator] - average_1
        yi_ya = array2[iterator] - average_2
        numerator += xi_xa * yi_ya
        denominator_x += xi_xa ** 2
        denominator_y += yi_ya ** 2
    return numerator / (denominator_x ** 0.5) * (denominator_y ** 0.5)


_data = pandas.read_excel("Q2_data.xlsx")
data = []

temperature_difference = get_temperate_difference(_data[0], _data[1])
temperature_difference = get_related_size(temperature_difference)[0]

data.append(temperature_difference)
for i in range(2, len(list(_data))):
    data.append(get_related_size(_data[i])[0])
print(data)

C_list = []

for column_index in range(len(data)):
    column = data[column_index]
    standard_difference = get_standard_difference(column)

    R = 0
    for r_index in range(len(data)):
        R += 1 - get_r(column, data[r_index])

    C = standard_difference * R
    C_list.append(C)

C_total = sum(C_list)
W_list = []
for C in C_list:
    W_list.append(C/C_total)

for W in W_list:
    print(W)
