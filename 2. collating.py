import pandas
import numpy

states = ['Alabama',
          'Arizona',
          'Arkansas',
          'California',
          'Colorado',
          'Connecticut ',
          'Florida',
          'Georgia',
          'Hawaii',
          'Idaho',
          'Illinois',
          'Indiana',
          'Iowa',
          'Kansas',
          'Kentucky',
          'Louisiana',
          'Maine',
          'Maryland',
          'Massachusetts ',
          'Michigan',
          'Minnesota',
          'Mississippi',
          'Missouri',
          'Montana',
          'Nebraska',
          'New Jersey',
          'New Mexico',
          'New York',
          'North Carolina',
          'North Dakota',
          'Ohio ',
          'Oklahoma',
          'Oregon',
          'Pennsylvania',
          'South Carolina',
          'South Dakota',
          'Tennessee ',
          'Texas',
          'Utah',
          'Vermont',
          'Virginia',
          'Washington',
          'West Virginia',
          'Wisconsin',
          'Wyoming',
          'Other States',
          'United States']

data_file_names = [r'2015-2016.xlsx']

data = pandas.read_excel(r"./handled.xlsx", sheet_name=None)
dates = list(data)
print(dates)

print("-------------------")

for i in range(0, len(states)):
    frame = pandas.DataFrame(numpy.zeros((len(dates), 2)))

    for j in range(0, len(dates)):
        frame[0][j] = dates[j]
        frame[1][j] = data[dates[j]][1][i]

    with pandas.ExcelWriter("handled_twice.xlsx", mode="a") as writer:
        frame.to_excel(writer, sheet_name=states[i])
