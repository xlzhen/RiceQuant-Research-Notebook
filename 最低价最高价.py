import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import datetime
from datetime import timedelta
from datetime import date

end_date = datetime.datetime.now() - timedelta(days=367)
#调取300天之前#

start_date = end_date - timedelta(days=1)
#变量days 设为11，起始时间11天前#

stock_ids = all_instruments(type="CS").order_book_id   
#调取股票（CS）库中所有股票ID，存入stocks_ids表#

num_stocks = len(stock_ids)
#用len（）函数获得股票个数#

list_s = []
#建立空表1#

number_of_stocks = 0

for stock_id in stock_ids:
      
        
      #遍历stock_ids中股票ID，股票ID存为stock_id
      p = get_price(stock_id, start_date, end_date, frequency = "1d", fields=['high', 'low', 'volume'], adjust_type='none')
      #get_price函数获取该股票价格，frequency设置为1天#
   
      a = len(p['high'])-1
      #当天天数序列号#
  
      count = 0 #不为0的成交量#
      i = 0
      #condition_one = 0
    
      if a > 0:

            #条件1:前一日成交量*130% >（i + 1） > i的成交量 #  
            if p['volume'][a-1]*2 > p['volume'][a] and p['volume'][a] > p['volume'][a-1]:
            #条件1:前一日成交量*130% >（i + 1） > i的成交量 #  

                #条件2：前10天平均200% i+1 10天平均120% #
                p2 = get_price(stock_id, end_date - timedelta(days = 11), end_date, frequency = "1d", fields=['close','volume'], adjust_type='none')
                b = len(p2['volume']) - 1
    
                count2 = 0
                j = 0
                sum = 0
                avg = 0
    
                if b > 0:
    
                #筛去0成交量#
                    while j <= b:
                          if p2['volume'][j] != 0: 
                                sum = sum + p2['volume'][j] 
                                count2 = count2 + 1
                          j = j + 1
                #筛去0成交量#
    
                    if count2 > 0:    
                          avg = (sum - p2['volume'][b])/(count2-1)    #过去10天内平均成交量#
    
                          if avg*2 > p['volume'][a] and p['volume'][a] > avg*1.2:

                
                #条件2：前10天平均200% i+1 10天平均120% #   
                                while i < a:
                                    if p['high'][i+1] != p['low'][i+1]: #排除当天一个价#
                                            if p['high'][i] < p['low'][i+1]:
                                    #compare p['high'][i+1] to p['low'][i+2 ... i + 31]#
                                                count = count + 1
                                                break
                                    i = i + 1
                #筛去0成交量#
    
                                if count > 0:    
                                    print(stock_id)                   #输出股票ID#
                                    list_s.append([stock_id])  #加入输出表#
                                    number_of_stocks = number_of_stocks + 1
        

          
df = pd.DataFrame(list_s) #转换为panda dataframe#
df.to_csv('最低价最高价.csv')      #输出至out.csv#
print(number_of_stocks)
print("done")             #结束提示#

