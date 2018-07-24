import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import datetime
from datetime import timedelta
from datetime import date


end_date = datetime.datetime.now() - timedelta(days=0) 

start_date = end_date - timedelta(days=1)

BACK_TRACK_DATE = end_date - timedelta(days=30)

def check_if_highest(stock_id, START_DATE, END_DATE):
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
            return [max_price, stock_close]
        else: return False    
    
    
    
def main():

    print("start")
    stock_ids = all_instruments(type="CS").order_book_id   
    num_stocks = len(stock_ids)
    list_s = []
    number_of_stocks = 0
    num_of_trade_days = 0 
    
    for stock_id in stock_ids:
          status = False
          stock_max_in_past_180 = ""
          current_close = ""
          temp = [0,0]
        
          p = get_price(stock_id, start_date, end_date, frequency = "1d", fields=['high', 'low', 'volume'], adjust_type='none')
          if not p is None:
              num_of_trade_days = len(p['volume'])-1
              count = 0 
              count3 = 0 
              i = 0
    
              if num_of_trade_days > 0:
                    if p['volume'][num_of_trade_days-1]*2 > p['volume'][num_of_trade_days] and p['volume'][num_of_trade_days] > p['volume'][num_of_trade_days-1]:
                            avg = avg_volume(stock_id)
                            if avg > 0: 
                                    if avg*2.7 > p['volume'][num_of_trade_days] and p['volume'][num_of_trade_days] > avg*1.2:
                                        while i < num_of_trade_days:
                                            if p['high'][i+1] != p['low'][i+1]: 
                                                    if p['high'][i] < p['low'][i+1]:
                                                            temp = check_if_highest(stock_id, BACK_TRACK_DATE, end_date)
                                                            if not temp is False:
                                                                status = True
                                                                stock_max_in_past_180 = temp[0]
                                                                current_close = temp[1]
                                                            else: status = False   
                                                            count = count + 1
                                                            break
                                            i = i + 1
    
                                        if count > 0:    
                                            list_s.append([stock_id, status, stock_max_in_past_180,current_close]) 
                                            number_of_stocks = number_of_stocks + 1
          
    df = pd.DataFrame(list_s) 
    df.rename(columns={0: '股票代码', 1:'是否超过', 2:'最高价', 3:'最低价'}, inplace=True)                                                      
    df.to_csv('strtgy_n_wth_bcktrck.csv') 
    print("done")           


def avg_volume(stock_id):
    p2 = get_price(stock_id, end_date - timedelta(days = 11), end_date, frequency = "1d", fields=['high','volume'], adjust_type='none')
    b = len(p2['volume']) - 1
    count2 = 0
    j = 0
    sum = 0
    avg = 0
    if b > 0:
            while j <= b:
                    if p2['volume'][j] != 0: 
                        sum = sum + p2['volume'][j] 
                        count2 = count2 + 1
                    j = j + 1
    
            if count2 > 0:    
                    return (sum - p2['volume'][b])/(count2-1)  
    else: return 0

def count_time(stock_id, high, start_index):
    count = 0 
    p3 = get_price(stock_id, start_date, twenty_after_end_date, frequency = "1d", fields=['high','volume'], adjust_type='none')
    num_of_trade_days = len(p3['volume']) - 1
    k = 0
    while start_index+k+1 <= num_of_trade_days and k < 16:
        if p3['high'][start_index+1+k] > high:
                count = count + 1
        k = k + 1
    return count


if __name__ == "__main__":
    main()


