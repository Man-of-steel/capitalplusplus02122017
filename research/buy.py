import pandas as pd
from pandas import DataFrame


def find_buy_signals(data_set_csv_file, row_from, row_to, target_change=0.0036, stop_loss_change=-0.0012):
    file_data = pd.read_csv(data_set_csv_file, header=None)
    data = DataFrame(data=file_data.iloc[row_from:row_to])
    data.index = range(0, 361)
    # print(data)
    potential_buys = []
    for index, series in data.iterrows():
        for i, new_series in DataFrame(data=data.iloc[index:]).iterrows():
            pos_delta = (new_series.iloc[4] - series.iloc[6])/series.iloc[6]
            neg_delta = (new_series.iloc[5] - series.iloc[6])/series.iloc[6]

            if pos_delta >= target_change:
                potential_buys.append(series.iloc[2])
                break

            if neg_delta <= stop_loss_change:
                break
    print('Number of potential buy signals: ' + str(len(potential_buys)))
    print('Potential Buy signals:\n' + str(potential_buys))
    print('Day details')
    day_open = data.iloc[0].iloc[3]
    day_close = data.iloc[360].iloc[3]
    day_change = ((day_close - day_open) / day_open) * 100
    print('Day open :', day_open)
    print('Day close :', day_close)
    print('Day change :', day_change, '%')
    return potential_buys

find_buy_signals(data_set_csv_file='G:\\Capital++\\historical_stock_data\\JUBLFOOD_03_Jul_to_20Jul2015.csv',
                 row_from=14, row_to=375)
