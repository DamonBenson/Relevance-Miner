# -*- coding: utf-8 -*-
##
#  @file "DateACK_Init.py"  
#  @brief "初始化数据库信息"
#  @brief "把已经爬取的日期记录下来"      
#  @author "Bernard "  
#  @date "2019-5-25"  
import pymysql
import datetime
def ACK_Init(ACK,MySQLInfo):
    Init(ACK,MySQLInfo['HOST'],MySQLInfo['USER'],MySQLInfo['PASSWORD'],MySQLInfo['PORT'])
def Init(ACK,
                DB_HOST_ADDRESS='127.0.0.1',
                DB_USER='root',
                DB_PASSWORD='123456',
                DB_PORT=3306):
    conn = pymysql.connect(host=DB_HOST_ADDRESS, user=DB_USER,passwd=DB_PASSWORD, port=DB_PORT)
    cur = conn.cursor()
    cur.execute('use keystock;')
    sql="SELECT Annc_DATE FROM keystock.dateinfo WHERE(dateinfo.DATE_ACK=1);"
    cur.execute(sql)
    conn.commit()
    results=cur.fetchall()
    cur.close()
    conn.close()
    for i in results:
        #print(i[0])
        t=i[0].strftime("%Y%m%d")#t 是字符串
        #print(t)
        if i not in ACK:
                ACK.append(t)
        # d=datetime.datetime.strptime(t, "%Y-%m-%d")
        # print(d)
    print('DateACK')
    print(ACK)
if __name__ == "__main__":
        DateACK=[]
        Init(DateACK)
        print(DateACK)    
        
        
        
        
        
        
# #把datetime转成字符串
# def datetime_toString(dt):
#     return dt.strftime("%Y-%m-%d-%H")

# #把字符串转成datetime
# def string_toDatetime(string):
#     return datetime.strptime(string, "%Y-%m-%d-%H")

# #把字符串转成时间戳形式
# def string_toTimestamp(strTime):
#     return time.mktime(string_toDatetime(strTime).timetuple())

# #把时间戳转成字符串形式
# def timestamp_toString(stamp):
#     return time.strftime("%Y-%m-%d-%H", tiem.localtime(stamp))

# #把datetime类型转外时间戳形式
# def datetime_toTimestamp(dateTim):
#     return time.mktime(dateTim.timetuple())
