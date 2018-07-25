'''
MACD dummy  
'''

import talib
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import datetime
from datetime import timedelta
from datetime import date

SHORTPERIOD = 12
LONGPERIOD = 26
SMOOTHPERIOD = 9
OBSERVATION = 100
s1 = "300036.XSHE"
END_DATE = datetime.datetime.now() - timedelta(days=2) 
START_DATE = END_DATE - timedelta(days=100)

def main():
    print(s1)
    prices = get_price(s1, START_DATE, END_DATE, frequency = "1d", fields=['volume','close'], adjust_type='none')
    prices[prices['volume']==0]=np.nan
    prices= prices.dropna()
    macd, signal, hist = talib.MACD(prices['close'].values, SHORTPERIOD,
                                    LONGPERIOD, SMOOTHPERIOD)
    
    print(macd[-1] - signal[-1])
    print(macd[-2] - signal[-2])
    
    if macd[-1] - signal[-1] < 0 and macd[-2] - signal[-2] < 0:
        print("出")
    
    if macd[-1] - signal[-1] > 0 and macd[-2] - signal[-2] > 0:
        print("入")
        
    print("end")

if __name__ == "__main__":
    main()
