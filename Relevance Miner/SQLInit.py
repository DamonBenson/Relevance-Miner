# -*- coding: utf-8 -*-
##
#  @file "SQLInit.py"  
#  @brief "数据库创建"     
#  @author "Bernard "  
#  @date "2019-5-21" 
import pymysql
def SQLInit(MySQLInfo):
    Create(MySQLInfo['HOST'],MySQLInfo['USER'],MySQLInfo['PASSWORD'],MySQLInfo['PORT'])
def Create(host="127.0.0.1", user="root",
                               passwd="123456", port=3306):
    conn = pymysql.connect(host="127.0.0.1", user="root",
                                passwd="123456", port=3306)
    cur = conn.cursor()
    #cur.execute('use Newstock;')
    #DROP DATABASE Newstock删除
    sql2='''
    CREATE SCHEMA IF NOT EXISTS Newstock CHARACTER SET utf8 COLLATE utf8_general_ci;
    USE Newstock;
    CREATE TABLE ANNC
    (
    ANNC_NO INT UNSIGNED PRIMARY KEY,
    ANNC_NAME varchar(255) COLLATE utf8_bin,
    ANNC_ADRESS varchar(255) COLLATE utf8_bin DEFAULT NULL
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE DATEINFO
    (
    ANNC_DATE DATE PRIMARY KEY,
    ANNC_NO INT UNSIGNED,
    FOREIGN KEY(ANNC_NO) REFERENCES ANNC(ANNC_NO)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE DATEINFO_DICT(
    ANNC_DATE DATE ,
    DATE_DICT_WORD varchar(32) COLLATE utf8_bin ,
    PRIMARY KEY(ANNC_DATE,DATE_DICT_WORD),
    DATE_DICT_WNUM INT UNSIGNED DEFAULT 0,
    FOREIGN KEY(ANNC_DATE) REFERENCES DATEINFO(ANNC_DATE)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE DATEINFO_ACK
    (
    ANNC_DATE DATE PRIMARY KEY,
    DATE_ACK tinyint DEFAULT 0,
    FOREIGN KEY(ANNC_DATE) REFERENCES DATEINFO(ANNC_DATE)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE ANNC_DICT (
    ANNC_NO INT UNSIGNED ,
    ANNC_DICT_WORD varchar(32)  COLLATE utf8_bin ,
    PRIMARY KEY(ANNC_NO,ANNC_DICT_WORD),
    ANNC_DICT_WNUM INT UNSIGNED DEFAULT 0,
    FOREIGN KEY(ANNC_NO) REFERENCES ANNC(ANNC_NO)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    CREATE TABLE BLACK_List (
    Dict_NO INT UNSIGNED PRIMARY KEY,
    Dict_WNUM varchar(32)  COLLATE utf8_bin ,
    Dict_OC tinyint DEFAULT 0
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
    '''
    i=0
    try:
        for str in sql2.split(';'):
            i=i+1
            if len(str)>=10:#防止空指令
                print (str)
                print (i)
                cur.execute(str)
                conn.commit()
                results=cur.fetchall()
    except:
        pass
    cur.close()
    conn.close()
####测试####
if __name__ == "__main__":
        ################### 读取配置文件 ###########################
    import ConfigParser  
    #生成config对象  
    conf = ConfigParser.ConfigParser()  
    #用config对象读取配置文件  
    conf.read("config.cfg")
    # 赋值
    #数据库
    # DB_HOST_ADDRESS = conf.get('database', 'host_address')
    # DB_USER =conf.get('database', 'user')
    # DB_PASSWORD =conf.get('database', 'password')
    # DB_PORT = int(conf.get('database', 'port'))

    # MySQLInfo={
    # 'HOST':DB_HOST_ADDRESS ,
    # 'USER':DB_USER,
    # 'PASSWORD':DB_PASSWORD ,
    # 'PORT':DB_PORT 
    # }
    Create()