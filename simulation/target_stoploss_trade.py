import pandas as pd
from utilities.moving_averages import simple_moving_average

capital = 100000
liquid_fund = capital
profit = 0
buy_quantity = sell_quantity = 0
brokerage = 50
target_change = 0.0044
stoploss_change = 0.003


def reached_target(bought_price, current_price):
    # print('Reached target function called at ' + str(bought_price) + ' and ' + str(current_price))
    # print('Delta : ' + str(current_price - bought_price))
    print('Percentage change = ' + str((current_price-bought_price)/bought_price))
    if current_price >= (bought_price + (bought_price * target_change)):
        return True
    else:
        return False


def hit_stoploss(bought_price, current_price):
    if current_price <= (bought_price - (bought_price * stoploss_change)):
        return True
    else:
        return False

data_set_file = 'BHARTIARTL.csv'
row_from = 15
row_to = 375
col = 6
file_data = pd.read_csv('G:\\Capital++\\historical_stock_data\\' + data_set_file)
one_minute_intraday_data_series = file_data.iloc[row_from:row_to, col] # specifically getting 15-Sep-2015 entire day data
one_minute_intraday_data = one_minute_intraday_data_series.tolist()

live_data = []
log = open('G:\\Capital++\\docs\\log.txt', 'w')
bigger_span = 20
smaller_span = 3
buy_price = 0
fresh = True
for i in range(360):
    live_data.append(one_minute_intraday_data[i])

    if len(live_data) <= bigger_span:
        continue

    if simple_moving_average(live_data, smaller_span) > simple_moving_average(live_data, bigger_span) and fresh:
        latest_price = live_data[i]
        buy_quantity = int(liquid_fund/latest_price)
        liquid_fund -= buy_quantity*latest_price
        buy_price = latest_price
        log.write('Bought ' + str(buy_quantity) + ' stocks at Rs.' + str(latest_price)
                  + ' each. Liquid fund spent : ' + str(buy_quantity*latest_price)
                  + ", Funds left : " + str(liquid_fund) + "\n-------\n")
        fresh = False

    if not fresh:
        latest_price = live_data[i]
        if reached_target(buy_price, latest_price) or hit_stoploss(buy_price, latest_price):
            sell_quantity = buy_quantity
            liquid_fund += sell_quantity * latest_price
            profit = liquid_fund - capital
            log.write('Sold ' + str(sell_quantity) + ' stocks at Rs.' + str(latest_price)
                      + ' each. Funds gained : ' + str(sell_quantity * latest_price)
                      + ", Liquid fund left : " + str(liquid_fund) + "\n---------------\n\n")
            fresh = True
log.close()
print('Funds left ' + str(liquid_fund))
print('Profit ' + str(profit))

