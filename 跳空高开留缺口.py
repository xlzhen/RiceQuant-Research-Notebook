import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import datetime
from datetime import timedelta
from datetime import date

END_DATE = datetime.datetime.now() - timedelta(days=412)                        #结束日/当前设置为412天之前#
TWENTY_AFTER_END_DATE = END_DATE + timedelta(days=20)                           #结束日之后预留20天#
START_DATE = END_DATE - timedelta(days=5)                                       #变量days 设为5，起始时间5天前#
    
def main():

    # print("start")                                                            #开始提示
    stock_ids = all_instruments(type="CS").order_book_id                        #调取股票（CS）库中所有股票ID，存入stocks_ids表#
    num_stocks = len(stock_ids)                                                 #用len（）函数获得股票个数#
    list_s = []                                                                 #建立空表1#
    number_of_stocks = 0
    num_of_trade_days = 0                                                       #交易天数

    for stock_id in stock_ids:                                                  #遍历stock_ids中股票ID，股票ID存为stock_id
          p = get_price(stock_id, start_date, end_date, frequency = "1d", fields=['high', 'low', 'volume'], adjust_type='none')
                                                                                #get_price函数获取该股票价格，frequency设置为1天
          if not p is None:
              num_of_trade_days = len(p['volume'])-1                            #当天天数序列号#
              count = 0                                                         #不为0的成交量#
              count3 = 0                                                        #跳空天最高价小于过后20天最高价的次数
              i = 0
    
              if num_of_trade_days > 0:
                    #条件1:前一日成交量*130% >（i + 1） > i的成交量 #  
                    if p['volume'][num_of_trade_days-1]*2 > p['volume'][num_of_trade_days] and p['volume'][num_of_trade_days] > p['volume'][num_of_trade_days-1]:
                    #条件1:前一日成交量*130% >（i + 1） > i的成交量 #  
                            avg = avg_volume(stock_id)                          #计算平均成交量 #
                            if avg > 0:                                         
                                    #条件2：前10天平均200% i+1 10天平均120% #
                                    if avg*2 > p['volume'][num_of_trade_days] and p['volume'][num_of_trade_days] > avg*1.2:
                                    #条件2：前10天平均200% i+1 10天平均120% #
                                        while i < num_of_trade_days:
                                            if p['high'][i+1] != p['low'][i+1]: #排除当天一个价#
                                                    if p['high'][i] < p['low'][i+1]:
                                                        count3 = count_time(stock_id, p['high'][i+1],i)
                                                        count = count + 1
                                                        break
                                            i = i + 1
    
                                        if count > 0:                           #如果存在跳空
                                            list_s.append([stock_id,count3])    #加入输出表#
                                            number_of_stocks = number_of_stocks + 1
          
    df = pd.DataFrame(list_s)                                                   #转换为panda dataframe
    df.rename(columns={0: '股票代码', 1: '超过次数'}, inplace=True) 
    df.to_csv('跳空高开留缺口.csv') 
    # print(number_of_stocks)
    # print("done")                                                             #结束提示

#计算平均成交量 
def avg_volume(stock_id):
    p2 = get_price(stock_id, end_date - timedelta(days = 11), end_date, frequency = "1d", fields=['high','volume'], adjust_type='none')
    b = len(p2['volume']) - 1
    count2 = 0
    j = 0
    sum = 0
    avg = 0
    if b > 0:
            #筛去0成交量
            while j <= b:
                    if p2['volume'][j] != 0: 
                        sum = sum + p2['volume'][j] 
                        count2 = count2 + 1
                    j = j + 1
            #筛去0成交量
    
            if count2 > 0:    
                    return (sum - p2['volume'][b])/(count2-1)                   #过去10天内平均成交量
    else: return 0
#计算平均成交量 #

#计算跳空当天最高价高于过后20天最高价次数
def count_time(stock_id, high, start_index):
    count = 0                                                                   #出现次数#
    p3 = get_price(stock_id, start_date, twenty_after_end_date, frequency = "1d", fields=['high','volume'], adjust_type='none')
    num_of_trade_days = len(p3['volume']) - 1                                   #交易天数
    k = 0
    while start_index+k+1 <= num_of_trade_days and k < 16:
        if p3['high'][start_index+1+k] > high:
                count = count + 1
        k = k + 1
    return count
#计算跳空当天最高价高于过后20天最高价次数


if __name__ == "__main__":
    main()
