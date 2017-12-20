import pandas as pd
from research import candlestick as cs
from research import strategies


def reached_target(bought_price, current_price, target_change):
    if current_price >= (bought_price + (bought_price * target_change)):
        return True
    else:
        return False


def hit_stoploss(bought_price, current_price, stop_loss_change):
    if current_price <= (bought_price - (bought_price * stop_loss_change)):
        return True
    else:
        return False


def simulate_trade(data_set_csv_file, row_from, row_to,
                   target_change=0.0012, stop_loss_change=0.0008):
    capital = 100000
    liquid_fund = capital
    profit = 0
    buy_quantity = sell_quantity = 0
    brokerage = 50
    file_data = pd.read_csv(data_set_csv_file, header=None)
    data = file_data.iloc[row_from:row_to]  # getting intra-day data
    data.index = range(361)
    # print(data)

    log = open('G:\\Capital++\\docs\\log.txt', 'w')
    buy_price = 0
    fresh = True
    funds_spent = funds_gained = 0

    for i in range(1, 361):
        if fresh:
            c1 = cs.CandleStick(data.iloc[i-1].iloc[3], data.iloc[i-1].iloc[4], data.iloc[i-1].iloc[5], data.iloc[i-1].iloc[6])
            c2 = cs.CandleStick(data.iloc[i].iloc[3], data.iloc[i].iloc[4], data.iloc[i].iloc[5], data.iloc[i].iloc[6])

            if strategies.is_bullish_engulfing(c1, c2):
                buy_price = int(c2.close)
                buy_quantity = liquid_fund // buy_price
                funds_spent = buy_quantity * buy_price
                liquid_fund -= funds_spent
                fresh = False
                log.write('Buy Quantity:' + str(buy_quantity) + '\nPrice:'+ str(buy_price) +
                          '\nFunds Spent:' + str(funds_spent) + '\nFunds Left:' + str(liquid_fund) + '\n----\n')
        else:
            high = data.iloc[i].iloc[4]
            low = data.iloc[i].iloc[5]

            if reached_target(buy_price, high, target_change):
                sell_price = high
                sell_quantity = buy_quantity
                funds_gained = sell_quantity * sell_price
                liquid_fund += funds_gained
                profit += funds_gained - funds_spent
                fresh = True
                log.write('Sell Quantity:' + str(sell_quantity) + '\nPrice:' + str(sell_price) +
                          '\nFunds Gained:' + str(funds_gained) + '\nFunds Left:' + str(liquid_fund)
                          + '\nProfit:' + str(profit) + '\n----Profit Trade-----\n\n')
                continue

            if hit_stoploss(buy_price, low, stop_loss_change):
                sell_price = low
                sell_quantity = buy_quantity
                funds_gained = sell_quantity * sell_price
                liquid_fund += funds_gained
                profit += funds_gained - funds_spent
                fresh = True
                log.write('Sell Quantity:' + str(sell_quantity) + '\nPrice:' + str(sell_price) +
                          '\nFunds Gained:' + str(funds_gained) + '\nFunds Left:' + str(liquid_fund) +
                          '\nProfit:' + str(profit) + '\n----Loss Trade-----\n\n')
                continue

    log.close()
    # print('Funds left ' + str(liquid_fund))
    print('Profit ' + str(profit))

    return profit


simulate_trade(data_set_csv_file='G:\\Capital++\\historical_stock_data\\JUBLFOOD_03_Jul_to_20Jul2015.csv',
               row_from=2997, row_to=3358)