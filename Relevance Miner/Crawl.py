# -*- coding: utf-8 -*-
##
#  @file "Crawl.py"  
#  @brief "爬虫"
#  @brief "负责爬取PDF公告并处理公告在存到数据库里"      
#  @author "Bernard "  
#  @date "2019-5-11"  
#http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice
#http://www.cninfo.com.cn/new/announcement/download?bulletinId=1206323143&announceTime=2019-06-01
import requests
import time
import re
import os
import InfoToMySQL
#import pymysql##该网站有些日期的数据缺失如果发现自动写入数据库，缺失日以查询。
WRONGPATH=['\/','\|','\\"','\?','\<','\>']  #错误路径
#WRONGPATH=['\\','\|','\\"','\?','\<','\>','\:']#错误路径
## Crawl
# 没有词频数据，爬取，处理，存入数据库
# @type   DateCrawl : list ["YYYYMMDD","YYYYMMDD"......]
# @param  DateCrawl : 需要爬取的日期
def Crawl(DateCrawl,
          path=ur'主函数\爬取文件',
          MySQLInfo=''):
    print(u"开始爬取")
    print(DateCrawl)
    CrawlNo=0
    url = "http://www.cninfo.com.cn/search/search.jsp"
    head = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
    'Cache-Control': 'max-age=0',
    'Cookie': '_sp_id.2141=f7c2f700-0937-4286-b4b9-a8bc33ff7a20.1559369763.2.1559373477.1559371047.f1a9fd03-531d-419c-a1b8-880124b204a7; insert_cookie=45380249; JSESSIONID=3A0A4AEA898E8A19F6A3FAC903143ABC',
    'Host': 'www.cninfo.com.cn',
    'Proxy-Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    pattern = re.compile(r'pageCount=(.*?);')
    resultpattern = re.compile(r'finalpage/(.*?)/(.*?).PDF" target=new>(.*?)</a>')
    for Date in DateCrawl:
        Date=Date[0:4]+'-'+Date[4:6]+'-'+Date[6:8]
        result=[]
        print("全新的一天")
        print(Date)
        value = {'endTime':Date,
          'startTime':Date,
           'pageNo':'1'}
        response = requests.post(url, value, headers=head)
        content = response.content
        print(content)
        #content=content.decode('gbk').encode('utf-8')
        pageCount = pattern.search(content).groups()[0]
        print(pageCount)
        pageCount = eval(pageCount)
        if pageCount==0:
            CrawlNo=CrawlNo+1
            continue
        

        ###寻找每一页里的url###
        pageNo = 1
        while pageNo<=pageCount:
            value['pageNo'] = '%d'%pageNo
            #print('发送')
            response = requests.post(url, value, headers=head)
            content = response.content
            result.extend(resultpattern.findall(content))
            print(pageNo)
            pageNo = pageNo+1
        ###爬取前先创文件夹###
        print(u'打开文件')
        TarDir= path+'\\'+Date#输出文件夹
        if not os.path.exists(TarDir):#创建输出文件夹
            os.mkdir(TarDir)
        total=len(result)#总共要下载
        num=0#目前下载了
        #print('下载')
        ###下载url里的pdf###
        for i in result:
            #print (i)
            downurl="http://www.cninfo.com.cn/new/announcement/download?bulletinId=%s&announceTime=%s"%(i[1],i[0])
            #print i[2]
            #print type(i[2])
            
            try:
                si=unicode(i[2],"utf8")
            except:
                si=unicode(i[2],"gbk")
            #print type(si)
            Dirpath=TarDir+'\\'+si+'.pdf'
            #print type(Dirpath)
            #Dirpath=Dirpath.encode("gbk")
            #print type(Dirpath)
            
            download(downurl, Dirpath)
            #print('下成功')
            num=num+1
            print('%d/%d'%(num,total))
        ###总算是爬取完了
        ###开始预存储###
        print(u"爬完啦哈哈哈")
        if total==0:#网址空文日
            pass
        else:
            DateFormat=('').join(Date.split('-'))#YYYYMMDD
            CrawlDate=[DateFormat]
            InfoToMySQL.InfoToMySQL(MySQLInfo, CrawlDate,path)
    #InfoToMySQL(SQLinfo,DateCrawled=['20190602'],   #要处理的日期
    #             DIR=u"F:\\2019sp\\Py\\源码\\手动爬取" ,  #路径):
    flag=(len(DateCrawl)==CrawlNo)#全网址空文日
    if flag:
        return False
    return True





def download(url,path,N=100000):
    try:
        r=requests.get(url)
    except:
        try:
            print('失败一次，重启中')
            time.sleep(20)
            print('重启后')
            r=requests.get(url)
        except:
            print('未知故障')
            print(url)
            return
    try:
        File = open(path, 'wb')
    except:
        try:
            print (path)
            path=re.sub('\*',u'星',path)
            for i in WRONGPATH:
                path=re.sub(i,u'：',path)
            print (path)
            File = open(path, 'wb')
        except:
            print(path)
            print('DownloadName Failed')
            return 
    for chunk in r.iter_content(N):
        File.write(chunk)
    File.close()
##测试##
#############BUG集合#########################
#content_txt = content_txt.decode('gbk').encode('utf-8')
#############################################
import datetime
import pandas as pd#进阶日期操作
##生成时间序列
def Datelist(beginDate, endDate):
        # beginDate, endDate是形如‘20160601’的字符串或datetime格式
        date_l=[datetime.datetime.strftime(x,'%Y%m%d')for x in list(pd.date_range(start=beginDate, end=endDate))]
        return date_l
if __name__ == "__main__":
    ################### 读取配置文件 ###########################
    import ConfigParser  
    #生成config对象  
    conf = ConfigParser.ConfigParser()  

    #用config对象读取配置文件  
    conf.read("config.cfg")
    sections = conf.sections()
    print(u'获取配置文件所有的section')
    print(sections)
    # 赋值
    #路径配置
    FILEPATH = conf.get('file', 'filepath')
    FILEPATH=FILEPATH.decode('utf-8')
    FILEPATH=FILEPATH.decode('utf-8')
    LOGPATH = conf.get('file', 'logpath')
    #数据库
    DB_HOST_ADDRESS = conf.get('database', 'host_address')
    DB_USER =conf.get('database', 'user')
    DB_PASSWORD =conf.get('database', 'password')
    DB_PORT = int(conf.get('database', 'port'))

    SQLInfo={
    'HOST':DB_HOST_ADDRESS ,
    'USER':DB_USER,
    'PASSWORD':DB_PASSWORD ,
    'PORT':DB_PORT 
    }
    #爬虫
    ############################################################
    DateCrawl=Datelist('20190522','20190531')
    #DateCrawl=Datelist('2019-05-31','2019-05-31')
    DateCrawl=['20190603']
    #DateCrawl=['2019-06-01','2019-06-02']
    path=ur'爬取文件'
    Crawl(DateCrawl,FILEPATH,SQLInfo)
