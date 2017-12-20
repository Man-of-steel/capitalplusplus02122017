import pandas as pd
from pandas import DataFrame
import time


def find_potential_buy_points(data_set_csv_file, row_from, row_to, target_change=0.0012, stop_loss_change=-0.0008):
    file_data = pd.read_csv(data_set_csv_file, header=None)
    data = DataFrame(data=file_data.iloc[row_from:row_to])
    data.index = range(0, 361)
    # print(data)
    potential_buys = []
    buy_sell_points = {}
    for index, series in data.iterrows():
        for i, new_series in DataFrame(data=data.iloc[index:]).iterrows():
            pos_delta = (new_series.iloc[4] - series.iloc[6])/series.iloc[6]
            neg_delta = (new_series.iloc[5] - series.iloc[6])/series.iloc[6]

            if pos_delta >= target_change:
                potential_buys.append(series.iloc[2])
                buy_sell_points[series.iloc[2]] = new_series.iloc[2]
                break

            if neg_delta <= stop_loss_change:
                break
    print('Total Number of potential buy signals: ', len(potential_buys))
    print('Potential Buy signals:\n', potential_buys)
    print('Buy-Sell points:\n', buy_sell_points)
    buy_sell_points = remove_in_betweens(buy_sell_points)
    print('After removing in betweens\n', buy_sell_points)
    print('Number of buy-sell points:', len(buy_sell_points))
    print('Day details')
    day_open = data.iloc[0].iloc[3]
    day_close = data.iloc[360].iloc[3]
    day_change = ((day_close - day_open) / day_open) * 100
    print('Day open :', day_open)
    print('Day close :', day_close)
    print('Day change :', day_change, '%')
    return potential_buys


def is_in_between(key, point1, point2):
    format = '%H:%M:%S'
    if time.strptime(point1, format) < time.strptime(key, format) < time.strptime(point2, format):
        return True
    else:
        return False


def remove_in_betweens(buy_sell_points):
    for key, value in buy_sell_points.copy().items():
        for k, v in buy_sell_points.copy().items():
            if is_in_between(k, key, value):
                del buy_sell_points[k]
    return buy_sell_points


find_potential_buy_points(data_set_csv_file='G:\\Capital++\\historical_stock_data\\INFY_08_Aug_2015_to_26_Aug_2015.csv',
                          row_from=389, row_to=750)
