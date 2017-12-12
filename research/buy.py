import pandas as pd


def find_buy_signals(data_set_csv_file, row_from, row_to, target_change=0.0036, stop_loss_change=0.0012):
    file_data = pd.read_csv(data_set_csv_file, header=None)
    data = file_data.iloc[row_from:row_to, :]
    potential_buys = []
    print(data.iloc[0:5].index)  # Stuck with problem of slicing a data frame based on real index
    for index, series in data.iterrows():
        for i, new_series in data.iloc[index:].iterrows():
            pos_delta = (new_series.iloc[4] - series.iloc[6])/series.iloc[6]
            neg_delta = (new_series.iloc[5] - series.iloc[6])/series.iloc[6]

            if pos_delta >= target_change:
                print('Adding ' + str(series.iloc[2]) + ' for target reach')
                potential_buys.append(series.iloc[2])
                break

            if neg_delta <= stop_loss_change:
                print('Exiting at ' + str(series.iloc[2]) + ' bcoz of stop loss hit')
                break
    print('Number of potential buy signals: ' + str(len(potential_buys)))
    print('Potential Buy signals:\n' + str(potential_buys))
    return potential_buys

find_buy_signals(data_set_csv_file='G:\\Capital++\\historical_stock_data\\JUBLFOOD_03_Jul_to_20Jul2015.csv',
                 row_from=764, row_to=1125)
