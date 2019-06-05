# -*- coding: utf-8 -*-
##
#  @file "MySQLGet.py"  
#  @brief "MySQL获取数据"
#  @brief "提取数据库内的词频信息*提取词频信息唯一函数*“      
#  @author "Bernard "  
#  @date "2019-5-30"
import pymysql
import datetime
import pandas as pd#进阶日期操作
##生成时间序列YYYY-MM-DD
def Datelist(beginDate, endDate):
       # beginDate, endDate是形如‘20160601’的字符串或datetime格式
       date_l=[datetime.datetime.strftime(x,'%Y%m%d')for x in list(pd.date_range(start=beginDate, end=endDate))]
       return date_l    
def MySQLGet(DateSE, MySQLInfo, DictDate, KEYA, KEYB, ANALYTYPE,SORTTYPE):
    DictDate.clear()#清空####***防止多次查询之间干扰***####
    SQL = []#指令集
    STARTDATE = 0
    ENDDATE = 1
    # ###YYYYMMDD转YYYY-MM-DD
    # Date[STARTDATE]=Date[STARTDATE][0:4]+'-'+Date[STARTDATE][4:6]+'-'+Date[STARTDATE][6:8]
    # Date[ENDDATE]=Date[ENDDATE][0:4]+'-'+Date[ENDDATE][4:6]+'-'+Date[ENDDATE][6:8]
    #登录数据库
    try:
        conn = pymysql.connect(host=MySQLInfo['HOST'], user=MySQLInfo['USER'],
                                    passwd=MySQLInfo['PASSWORD'], port=MySQLInfo['PORT'])
    except Exception as e:#登录失败
        print (e)
        print(MySQLInfo)
        return 
       
    cur = conn.cursor()
########开始查询######查询正常会有Result，开始更新数组
    if ANALYTYPE==1:#日期查询
        print("日期查询")
        if SORTTYPE==1:#最热##100个词
            sql='''SELECT KEYSTOCK.DATEINFO_DICT.DATE_DICT_WORD
                    FROM KEYSTOCK.DATEINFO_DICT 
                    WHERE KEYSTOCK.DATEINFO_DICT.ANNC_DATE<='%s'
                    AND KEYSTOCK.DATEINFO_DICT.ANNC_DATE>='%s'
                    ORDER BY DATEINFO_DICT.DATE_DICT_WNUM 
                    DESC LIMIT 100;'''%(DateSE[ENDDATE],DateSE[ENDDATE])##100个词
            try:
                ###执行语句
                cur.execute('use keystock;')
                print (sql)
                cur.execute(sql)
                conn.commit()
                Results=cur.fetchall()
                #return Results
            except Exception as e:#调试
                print (e)
                print(u'!!!!!!!异常!!!!!!!')
                print (sql)
            else:#正常执行try elses
                if Results:
                    ###结束查询
                    #print(u"查词语")
                    print(Results)
            for Item in Results:
                Dict=Item[0].decode('utf-8')
                DictDate[Dict]={}
                SingleDict={}
                sql='''SELECT KEYSTOCK.DATEINFO_DICT.ANNC_DATE,KEYSTOCK.DATEINFO_DICT.DATE_DICT_WNUM 
                        FROM KEYSTOCK.DATEINFO_DICT 
                        WHERE KEYSTOCK.DATEINFO_DICT.ANNC_DATE<='%s'
                        AND KEYSTOCK.DATEINFO_DICT.ANNC_DATE>='%s'
                        AND KEYSTOCK.DATEINFO_DICT.DATE_DICT_WORD='%s'
                        ORDER BY DATEINFO_DICT.DATE_DICT_WNUM ;'''%(DateSE[ENDDATE],DateSE[STARTDATE],Dict)
                try:
                    ###执行语句
                    cur.execute('use keystock;')
                    #print (sql)
                    cur.execute(sql)
                    conn.commit()
                    Results=cur.fetchall()
                except Exception as e:#调试
                    print (e)
                    print(u'!!!!!!!异常!!!!!!!')
                    print (sql)
                else:#正常执行
                    print(u"结束查询")
                    if Results:
                        for OneItem in Results:
                            DBDate=OneItem[0].strftime("%Y%m%d")#日期
                            DBDictNUM=OneItem[1]#词数
                            SingleDict={DBDate:DBDictNUM}
                            DictDate[Dict].update(SingleDict)
                        try:
                            del SingleDict
                        except:
                            pass
            cur.close()
            conn.close()
            return True
        else:#最快
              
            ###结束查询
            print(u"结束查询")
            cur.close()
            conn.close()
            return True


        
    else:#关键词查询
        for KEY in [KEYA,KEYB]:
            KEY=KEY.decode('utf-8')
            DictDate[KEY]={}
            sql='''SELECT KEYSTOCK.DATEINFO_DICT.ANNC_DATE,KEYSTOCK.DATEINFO_DICT.DATE_DICT_WORD,KEYSTOCK.DATEINFO_DICT.DATE_DICT_WNUM 
                    FROM KEYSTOCK.DATEINFO_DICT 
                    WHERE  KEYSTOCK.DATEINFO_DICT.ANNC_DATE<'%s'
                    AND KEYSTOCK.DATEINFO_DICT.ANNC_DATE>='%s'
                    AND KEYSTOCK.DATEINFO_DICT.DATE_DICT_WORD='%s'
                    ORDER BY DATEINFO_DICT.DATE_DICT_WNUM; '''%(DateSE[ENDDATE],DateSE[STARTDATE],KEY)
        # SQL.append(sql)
            try:
                ###执行语句
                cur.execute('use keystock;')
                print (sql)
                cur.execute(sql)
                conn.commit()
                Results=cur.fetchall()
            except Exception as e:#调试
                print (e)
                print(u'!!!!!!!异常!!!!!!!')
                print (sql)
            else:#结束查询
                print(u"结束查询")
                if Results:
                    for OneItem in Results:
                        DBDate=OneItem[0].strftime("%Y%m%d")#日期
                        DBDictNUM=OneItem[1]#词数
                        SingleDict={DBDate:DBDictNUM}
                        DictDate[KEY].update(SingleDict)
                    try:
                        del SingleDict
                    except:
                        pass
        cur.close()
        conn.close()
        return True#关键词成功
    return False#凉了
####测试####
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

    MySQLInfo={
    'HOST':DB_HOST_ADDRESS ,
    'USER':DB_USER,
    'PASSWORD':DB_PASSWORD ,
    'PORT':DB_PORT 
    }
    #爬虫
    ############################################################
    KEYA='芯片'
    KEYB='美国'
    ##decode('utf-8')
    ##encode('utf-8')
    SORTTYPE=1#1是最热 2是最快
    ANALYTYPE=1#1是时间，2是关键词
    DictDate={}
    DateSE=['20190501','20190531']
    result=MySQLGet(DateSE, MySQLInfo, DictDate, KEYA, KEYB, SORTTYPE=1, ANALYTYPE=2)
    print(DateSE)
