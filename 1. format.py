import pandas
import numpy

saved_data = pandas.DataFrame(numpy.zeros((50, 2)))
frames = pandas.read_excel(io=r"data.xlsx", sheet_name=None)
for i in list(frames):
    frame = frames[i]

    state_data = frame.loc[2][0]
    if type(state_data) != str:
        continue
    states = state_data.split("\n")
    for j in range(0, len(states)):
        saved_data[0][j] = states[j]
    data = frame.loc[2]
    for j in range(1, 2):
        if type(data[j]) != str:
            continue
        handled = data[j].split("\n")
        write = saved_data[1]
        for k in range(0, len(handled)):
            write[k] = handled[k]

    with pandas.ExcelWriter("handled.xlsx", mode="a") as writer:
        saved_data.to_excel(writer, sheet_name=i)

