# -*- coding: utf-8 -*-
##
#  @file "InfoSelect.py"  
#  @brief "词频日期信息提取"
#  @brief "获取词频信息，*所有获取信息的主控模块*“      
#  @author "Bernard "  
#  @date "2019-5-30"
import  Crawl##负责爬取资讯，内置资讯预处理函数*词频处理依赖结巴分词关键词*  
import  MySQLGet##"提取数据库内的词频信息*提取词频信息唯一函数*“  

def InfoSelect(DateCrawl,DictDate,path,DateSE,MySQLInfo,KEYA, KEYB, ANALYTYPE, SORTTYPE):
    print('获取词频信息')
    print(DateCrawl)
    if DateCrawl:#需要爬取
        #ProcessInfo.set("开始爬取")   
        # def Crawl(DateCrawl,#           path=ur'主函数\爬取文件',#           MySQLInfo=''):
        if Crawl.Crawl(DateCrawl,path,MySQLInfo) or True:#爬完再取
            #ProcessInfo.set("爬取完毕开始提取") 
        #def MySQLGet(DateSE, MySQLInfo, DictDate, KEYA, KEYB, ANALYTYPE,SORTTYPE):
            if MySQLGet.MySQLGet(DateSE,MySQLInfo,DictDate,KEYA, KEYB, ANALYTYPE, SORTTYPE):
                    #ProcessInfo.set("提取完成开始分析") 
                    return True
            else:#没get到任何东西
                    raise Exception("数据库为空")
                    return False
        else:#貌似出了什么岔子
           # raise Exception("爬取异常")
            return False
                

    else:#空不需要爬取
        #ProcessInfo.set("开始提取") 
        #def MySQLGet(DateSE, MySQLInfo, DictDate, KEYA, KEYB, ANALYTYPE,SORTTYPE):
        if MySQLGet.MySQLGet(DateSE,MySQLInfo,DictDate,KEYA, KEYB, ANALYTYPE, SORTTYPE):
                #ProcessInfo.set("提取完成开始分析") 
                return True
        else:#没get到任何东西
                raise Exception("数据库为空")
                return False


    