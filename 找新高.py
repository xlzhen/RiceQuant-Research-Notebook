import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import datetime
from datetime import timedelta
from datetime import date

END_DATE = datetime.datetime.now() - timedelta(days=0)  
#结束日/当前设置为今天#

START_DATE = END_DATE - timedelta(days=190)                               
#变量days 设为10，起始时间10天前#


# def check_in_order(p, index_start, index_end) return success index or False


def main():
    
    print("start")                                      
    # 开始提示
    stock_ids = all_instruments(type="CS").order_book_id   
    #调取股票（CS）库中所有股票ID，存入stocks_ids表#
    list_s = []
    #建立空表1#
    num_of_trade_days = 0 
    #交易天数
    
    for stock_id in stock_ids:
    #遍历stock_ids中股票ID，股票ID存为stock_id
          p = get_price(stock_id, START_DATE, END_DATE, frequency = "1d", fields=['high','low'], adjust_type='none')
          #get_price函数获取该股票最高价格，frequency设置为1天
          if not p is None:
               num_of_trade_days = p.iloc[:,0].size  #获取交易天数
               # check in order with 10 days
               # if index
                    #check in order with i-180 days
                    #if index2 == index return index
            
    
if __name__ == "__main__":
    main()
