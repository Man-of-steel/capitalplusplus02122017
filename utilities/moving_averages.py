import math

'''
Finding simple moving average 
by receiving data as a list 
and span as span
'''
def simple_moving_average(data, span=3):
    if len(data) < span:
        return data[len(data)-1]    # returning last item of list if not enough data provided to compute SMA
    required_data = data[-span:]  # slicing given list from end to only get span number of data
    sma = math.fsum(required_data)/len(required_data)
    return sma


data = [1.12, 2.23, 3.34, 4.45, 5.56]
print(simple_moving_average(data))
