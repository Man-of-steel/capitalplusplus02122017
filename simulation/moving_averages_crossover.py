capital = 100000
liquid_fund = capital
profit = 0
buy_quantity = sell_quantity = 0
brokerage = 50


import pandas as pd
from utilities.moving_averages import simple_moving_average
file_data = pd.read_csv('G:\\Capital++\\historical_stock_data\\INFY_12Sep2015_to_04Oct2015.csv')
one_minute_intraday_data_series = file_data.iloc[152:513, 6]   # specifically getting 15-Nov-2015 entire day data
one_minute_intraday_data = one_minute_intraday_data_series.tolist()

live_data = []
log = open('G:\\Capital++\\docs\\log.txt', 'a+')
bigger_span = 14
smaller_span = 3
fresh = True
for i in range(360):
    live_data.append(one_minute_intraday_data[i])

    if len(live_data) >= bigger_span:
        if simple_moving_average(live_data, smaller_span) > simple_moving_average(live_data, bigger_span) and fresh:
            latest_price = live_data[i]
            buy_quantity = liquid_fund/latest_price
            liquid_fund -= buy_quantity*latest_price
            log.write('Bought ' + str(buy_quantity) + ' stocks at Rs.' + str(latest_price)
                      + ' each. Liquid fund spent : ' + str(buy_quantity*latest_price)
                      + ", Funds left : " + str(liquid_fund))
            fresh = False

        if simple_moving_average(live_data, smaller_span) < simple_moving_average(live_data, bigger_span) and not fresh:
            latest_price = live_data[i]
            sell_quantity = buy_quantity
            liquid_fund = sell_quantity * latest_price
            profit = liquid_fund - capital
            log.write('Sold ' + str(sell_quantity) + ' stocks at Rs.' + str(latest_price)
                      + ' each. Funds gained : ' + str(sell_quantity * latest_price)
                      + ", Liquid fund left : " + str(liquid_fund))
            fresh = True

print('Funds left ' + str(liquid_fund))
print('Profit ' + str(profit))