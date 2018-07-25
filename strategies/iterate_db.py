'''
find all stocks at day i have highest price in past n days
'''

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import datetime
from datetime import timedelta
from datetime import date

END_DATE = datetime.datetime.now() - timedelta(days=0)

START_DATE = END_DATE - timedelta(days=181)

def main():
    print("start")
    stock_ids = all_instruments(type="CS").order_book_id
    
    result = []
    
    for stock_id in stock_ids:
        list_price_high = []
        stock_close = 0
        num_of_trade_days = 0
        
        p = get_price(stock_id, START_DATE, END_DATE, frequency = "1d", fields=['high','close'], adjust_type='none')

        if not p is None and not p.empty:
            num_of_trade_days = p.iloc[:,0].size - 1  
            i = 0
            while i < num_of_trade_days:
                list_price_high.append(p['high'][i])
                i = i + 1
            stock_close = p['close'][i]
            
            max_price = max(list_price_high)
    
            if(max_price < stock_close):
                result.append([stock_id, max_price, stock_close])
                status = True
            else: status = False
    
    df = pd.DataFrame(result)
    df.rename(columns={0: '股票代码', 1: '过去最高价', 2:'当日收盘价'}, inplace=True) 
    df.to_csv('iterate_db_hg.csv') 
    
    print("done")

if __name__ == "__main__":
    main()

