# -*- coding: utf-8 -*-
##
#  @file "DateCrawl_Init.py"  
#  @brief "初始化爬虫要爬取的日期"
#  @brief "把需要爬取的日期记录下来"      
#  @author "Bernard "  
#  @date "2019-5-25"  
import datetime
import pandas as pd#进阶日期操作
def Datelist(beginDate, endDate):##生成时间序列
        # beginDate, endDate是形如‘20160601’的字符串或datetime格式
        date_l=[datetime.datetime.strftime(x,'%Y%m%d')for x in list(pd.date_range(start=beginDate, end=endDate))]
        return date_l
def DateCrawlInitDefault(CycleLenth):#从昨天到前默认周期的天
        Today = datetime.date.today()#今天 
        StartDay= Today-datetime.timedelta(days = CycleLenth)#15天前开始
        StrStartDay=StartDay.strftime("%Y%m%d")#字符串化
        EndDay= Today-datetime.timedelta(days = 1)#昨天结束
        StrEndDay=EndDay.strftime("%Y%m%d")#字符串话
        return StrStartDay,StrEndDay
def DateCrawlInit(DateCrawl,DateACK,CycleLenth,StrStartDay='',StrEndDay='',FLAG=True):
        # if FLAG:
        #         [StrStartDay,StrEndDay]=DateCrawlInitDefault(CycleLenth)#从昨天到前默认周期的天
        # elif StrStartDay=='' or StrEndDay=='':
        #         raise Exception 
        while DateCrawl:##清空
                DateCrawl.pop()
        if StrStartDay=='' or StrEndDay=='':
                [StrStartDay,StrEndDay]=DateCrawlInitDefault(CycleLenth)#从昨天到前默认周期的天
        else:
                pass   
        print([StrStartDay,StrEndDay])
        DateCrawlTemp=Datelist(StrStartDay,StrEndDay)
        for i in DateCrawlTemp:
                if i not in DateACK:
                        DateCrawl.append(i)
        print(DateCrawl)
        return StrStartDay,StrEndDay
        
if __name__ == "__main__":
        DateACK=[]
        DateCrawl=[]
        DateCrawlInit(DateCrawl,DateACK)
        print(DateCrawl)
