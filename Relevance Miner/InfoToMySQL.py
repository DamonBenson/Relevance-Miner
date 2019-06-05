# -*- coding: utf-8 -*-
##
#  @file "InfoToMySQL.py"  
#  @brief "数据库存储"
#  @brief "数据存入数据库"    
#  @author "Bernard "  
#  @date "2019-5-30"  
import InfoPreprocessor
import pymysql

def InfoToMySQL(SQLInfo,DateCrawled,   #要处理的日期
                DIR #路径
                ):
    print(u"准备存储")
    for sqldate in DateCrawled:
        SQLDate=[sqldate]
        #try:
        #登录数据库
        try:
            conn = pymysql.connect(host=SQLInfo['HOST'], user=SQLInfo['USER'],
                                       passwd=SQLInfo['PASSWORD'], port=SQLInfo['PORT'])
        except:#失败调试
            print(SQLInfo)
        cur = conn.cursor()
        #获取日期字典，公告字典
        ###公告词典{日期：{标题：[词，词，词]，标题：[词，词，词]}}
        ###日期词典{日期：{词:词数,词:词数}}
        DateDict,DateAnncDict=InfoPreprocessor.InfoPreprocessor(DIR,SQLDate)   
        print(u"开始存储")
        
        ###初始化SQL语句
        SQL=[]
        for DateSel in DateAnncDict:#日期键
            
            No=1
            print(DateSel)
            Date=eval(DateSel)
            ##确认日期
            SQL.append('''INSERT INTO keystock.DATEINFO(ANNC_DATE,DATE_ACK)VALUES(%d,1)'''%(Date))
            for AnncSel in DateAnncDict[DateSel]:#标题键
                #print (type(AnncSel))# unicode
                Annc=AnncSel.encode('utf8')
                #print (type(Annc))# str
                temp=eval(DateSel[2:9])*10000#截取时间
                AnncNo=temp+No#190604+0001 公告标号
                PathSave=DIR+'\\'+Annc#存储地址
                #插入公告
                #插入公告日期关系
                SQL.append('''INSERT INTO keystock.annc(ANNC_NO,ANNC_NAME,ANNC_ADRESS) VALUES(%d,"%s","%s")'''%(AnncNo,Annc,PathSave))
                SQL.append('''INSERT INTO keystock.DATEANNC(ANNC_DATE,ANNC_NO) VALUES(%d,%d)'''%(Date,AnncNo))
                for DictSel in DateAnncDict[DateSel][AnncSel]:#词
                    #print(type(DictSel))
                    Dict=DictSel.encode('utf8')
                    SQL.append('''INSERT INTO keystock.annc_dict(ANNC_DICT_WORD,ANNC_NO,ANNC_DICT_WNUM) VALUES("%s",%d,1)'''%(Dict,AnncNo))
                print(No)
                No=No+1

        for DateSel in DateDict:#日期键
            #print(DateSel)
            Date=eval(DateSel)
            for DictSel in DateDict[DateSel]:#词键
                DictNumSel=DateDict[DateSel][DictSel]#词键值词数
                #print (type(DictSel))
                #print (DictNumSel)
                Dict=DictSel.encode('utf8')
                SQL.append('''INSERT INTO keystock.DATEINFO_DICT(DATE_DICT_WORD,ANNC_DATE,DATE_DICT_WNUM,Dict_OC) VALUES("%s",%d,%d,1)'''%(Dict,Date,DictNumSel))
        try:
            cur.execute('use keystock;')
            ###执行语句
            for sql in SQL:
                try:
                    #print (sql)
                    cur.execute(sql)
                    conn.commit()
                    results=cur.fetchall()
                except Exception as e:#调试
                    print (e)
                    print(u'!!!!!!!异常!!!!!!!')
                    #print(type(sql))   #str
                    print (sql)
                    print(u'!!!!!!!语句!!!!!!!')
                    pass
                else:#正常执行
                    if results:
                        print(results)
            
            ###结束存储
            print(u"结束存储")
            del DateDict
            del DateAnncDict
            cur.close()
            conn.close()
            #except:
            #else:
            print(u"完成存储")
        except Exception as e:#调试
            print(e)
    return True
##测试

import datetime
import pandas as pd#进阶日期操作
def Datelist(beginDate, endDate):##生成时间序列
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
    DateCrawl=Datelist('20190527','20190601')
    print (DateCrawl)
    #DateCrawl=['20190522']
    InfoToMySQL(SQLInfo=SQLInfo,DateCrawled=DateCrawl,DIR=FILEPATH)
