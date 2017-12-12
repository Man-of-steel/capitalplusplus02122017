import os
import pandas as pd
from utilities.moving_averages import simple_moving_average


def reached_target(bought_price, current_price, target_change):
    # print('Reached target function called at ' + str(bought_price) + ' and ' + str(current_price))
    # print('Delta : ' + str(current_price - bought_price))
    # print('Percentage change = ' + str((current_price-bought_price)/bought_price))
    if current_price >= (bought_price + (bought_price * target_change)):
        return True
    else:
        return False


def hit_stoploss(bought_price, current_price, stop_loss_change):
    if current_price <= (bought_price - (bought_price * stop_loss_change)):
        return True
    else:
        return False


def simulate_trade(data_set_csv_file, row_from, row_to, col,
                   target_change=0.0044, stop_loss_change=0.003, bigger_span=20, smaller_span=3):
    capital = 100000
    liquid_fund = capital
    profit = 0
    buy_quantity = sell_quantity = 0
    brokerage = 50
    file_data = pd.read_csv(data_set_csv_file, header=None)
    one_minute_intraday_data_series = file_data.iloc[row_from:row_to, col]  # getting intra-day data
    one_minute_intraday_data = one_minute_intraday_data_series.tolist()

    live_data = []
    log = open('G:\\Capital++\\docs\\log.txt', 'w')
    buy_price = 0
    fresh = True
    for i in range(360):
        live_data.append(one_minute_intraday_data[i])

        if len(live_data) <= bigger_span:
            continue

        if simple_moving_average(live_data, smaller_span) > simple_moving_average(live_data, bigger_span) and fresh:
            latest_price = live_data[i]
            buy_quantity = int(liquid_fund / latest_price)
            liquid_fund -= buy_quantity * latest_price
            buy_price = latest_price
            log.write('Bought ' + str(buy_quantity) + ' stocks at Rs.' + str(latest_price)
                      + ' each. Liquid fund spent : ' + str(buy_quantity * latest_price)
                      + ", Funds left : " + str(liquid_fund) + "\n-------\n")
            fresh = False

        if not fresh:
            latest_price = live_data[i]
            if reached_target(buy_price, latest_price, target_change) or hit_stoploss(buy_price, latest_price, stop_loss_change):
                sell_quantity = buy_quantity
                liquid_fund += sell_quantity * latest_price
                profit = liquid_fund - capital
                log.write('Sold ' + str(sell_quantity) + ' stocks at Rs.' + str(latest_price)
                          + ' each. Funds gained : ' + str(sell_quantity * latest_price)
                          + ", Liquid fund left : " + str(liquid_fund) + "\n---------------\n\n")
                fresh = True
    log.close()
    # print('Funds left ' + str(liquid_fund))
    print('Profit ' + str(profit))

    return profit


def optimize_and_log():
    log_file = "G:\\Capital++\\docs\\optimized_values.txt"
    data_set_dir = "G:\\Capital++\\historical_stock_data\\"

    log = open(log_file, 'a')
    all_files = os.listdir(data_set_dir)

    all_csv_files = []
    for f in all_files:
        if str(f).endswith('.csv'):
            all_csv_files.append(f)

simulate_trade(data_set_csv_file='G:\\Capital++\\historical_stock_data\\BHARTIARTL.csv',
               row_from=764, row_to=1124, col=6, target_change=0.0044, stop_loss_change=0.003)
