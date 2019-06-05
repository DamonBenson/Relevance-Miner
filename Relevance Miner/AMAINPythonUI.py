# -*- coding: utf-8 -*-
##
#  @file "AMAINPythonUI.py"  
#  @brief "主控制包括UI布局"
#  @brief "对收集到的词频信息，并根据制表要求进行指定卷积等数据操作，最后生成图表"      
#  @author "Bernard "  
#  @date "2019-5-11"       
import Tkinter as Tk#TK UI自带
import datetime #自带与时间操作有关
import MySQLdb#MySQL数据库需要安装
import pandas as pd#进阶日期操作
################### 自定义函数###########################
import Show#展示图窗，目前为空
import DateACK_Init##把已经爬取的日期记录下来
#ACK_Init(ACK,DB_HOST_ADDRESS='127.0.0.1',DB_USER='root',DB_PASSWORD=123456,DB_PORT=3306)#
import DateCrawl_Init##"把需要爬取的日期记录下来" 
#DateCrawlInit(DateCrawl,DateACK,FLAG=True,StrStartDay='',StrEndDay=''):#
import SQLInit#创建数据库
#def SQLInit(MySQLInfo):#
import InfoAnalysis#收集到的词频信息，并根据制表要求进行指定卷积等数据操作，最后生成图表
############################################################
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
#(MySQLInfo['HOST'],MySQLInfo['USER'],MySQLInfo['PASSWORD'],MySQLInfo['PORT'])
############################################################
###设置交互窗基础信息
root=Tk.Tk()
root.title('关联挖掘')                   #窗口名
root.configure(background='white')          #窗口背景色           
root.geometry('640x480')                   # 设置窗口大小
root.resizable(width=True, height=True)    # 设置窗口宽度可变，高度可变
###
################### 全局变量与常量 ###########################
###数据库的情况：我有那几天的数据
#已经拥有的资讯日期
DateACK = []##YYYYMMDD类型
###词频日期信息提取函数需要的参数
#要爬取的日期
DateCrawl = []##YYYYMMDD类型
##日期词频信息
DictDate = {}###{日期：{词:词数,词:词数}}###****关键数据结构***###



###划区
##  INPUTBACKGROUNDCOLOR输入区背景色
##  DISPLAYBACKGROUNDCOLOR展示区背景色
INPUTBACKGROUNDCOLOR="Wheat"#背景框颜色
DISPLAYBACKGROUNDCOLOR="LawnGreen"
LABELBACKGROUNDCOLOR="Chartreuse"#7FFF00 Chartreuse 黄绿色/查特酒绿 标签
BUTTONBACKGROUNDCOLOR='LightSkyBlue'#87CEFA LightSkyBlue 亮天蓝色   按钮
##  InputFrame 输入控制放置区
##  DisplayFrame 展示插件放置区
InputFrame=Tk.Frame(root, background=INPUTBACKGROUNDCOLOR)#声明
InputFrame.place(relx=0.0, rely=0.0, relwidth=1, relheight=1)#放置
# DisplayFrame=Tk.Frame(root, background=DISPLAYBACKGROUNDCOLOR)#声明
# DisplayFrame.place(relx=0.5, rely=0.0, relwidth=0.5, relheight=1)#放置
# ###

####*普通变量
###**图形交互信息
##周期长度枚举变量
class CYCLELENTH:
    TINY=7#周
    SMALL=15#两周 默认
    MEDIUM=30#一个月
    LARGE=90#一个季度
    HUGE=365#一年
##分析类型枚举变量
class ANALYTYPE:
    DATE=1#日期 默认
    DICT=2#关键词
##排序选择枚举变量
class SORTTYPE:
    HOT=1#最热 默认
    DENSITY=2#最快
##当前用户的制图要求，默认周期30析，类型默认时间，排序选择默认最热
UserRuir=[CYCLELENTH.SMALL,ANALYTYPE.DATE,SORTTYPE.HOT]

##上次用户的制图要求
LastUserRuir=UserRuir
###**



####*

###标签变量
##  @param ProcessInfo  #精度信息 type=Tkinter.StringVar()
ProcessInfo=Tk.StringVar()#进度信息
ConsoleInfo=Tk.StringVar()#错误信息
StartDate=Tk.StringVar()#开始日期
StartDateIn=Tk.StringVar()#开始日期输入中
EndDate=Tk.StringVar()#结束日期
EndDateIn=Tk.StringVar()#结束日期输入中
KeyA=Tk.StringVar()#关键词A
KeyAIn=Tk.StringVar()#关键词A输入中
KeyB=Tk.StringVar()#关键词B
KeyBIn=Tk.StringVar()#关键词B输入中
CycleLenth=Tk.StringVar()#选择周期的长度
SortType=Tk.StringVar()#选择排序类型
Cycle=Tk.StringVar()#设置周期的长度
Sort=Tk.StringVar()#设置排序类型
from InfoSelect import *#获取词频信息，*所有获取信息的主控模块*
Tk.Label(InputFrame,text='当前进度',background=LABELBACKGROUNDCOLOR).place(relx=0.05,rely=0.55,relwidth=0.20,relheight=0.10)
Tk.Label(InputFrame,textvariable=ProcessInfo).place(relx=0.05,rely=0.65,relwidth=0.20,relheight=0.10)
Tk.Label(InputFrame,text='调试信息',background=LABELBACKGROUNDCOLOR).place(relx=0.05,rely=0.75,relwidth=0.20,relheight=0.10)
Tk.Label(InputFrame,textvariable=ConsoleInfo).place(relx=0.05,rely=0.85,relwidth=0.20,relheight=0.10)

EntryStartDate=Tk.Entry(InputFrame,textvariable=StartDateIn)
EntryStartDate.place(relx=0.05,rely=0.15,relwidth=0.20,relheight=0.10)
Tk.Label(InputFrame,textvariable=StartDate,background=LABELBACKGROUNDCOLOR).place(relx=0.05,rely=0.05,relwidth=0.20,relheight=0.10)

EntryEndDate=Tk.Entry(InputFrame,textvariable=EndDateIn)
EntryEndDate.place(relx=0.30,rely=0.15,relwidth=0.20,relheight=0.10)
Tk.Label(InputFrame,textvariable=EndDate,background=LABELBACKGROUNDCOLOR).place(relx=0.30,rely=0.05,relwidth=0.20,relheight=0.10)

EntryKeyA=Tk.Entry(InputFrame,textvariable=KeyAIn)
EntryKeyA.place(relx=0.05,rely=0.40,relwidth=0.20,relheight=0.10)
Tk.Label(InputFrame,textvariable=KeyA,background=LABELBACKGROUNDCOLOR).place(relx=0.05,rely=0.30,relwidth=0.20,relheight=0.10)

EntryKeyB=Tk.Entry(InputFrame,textvariable=KeyBIn)
EntryKeyB.place(relx=0.30,rely=0.40,relwidth=0.20,relheight=0.10)
Tk.Label(InputFrame,textvariable=KeyB,background=LABELBACKGROUNDCOLOR).place(relx=0.30,rely=0.30,relwidth=0.20,relheight=0.10)
###text="关键词B:",text="关键词A:",text="日期:",text="日期:",
###初始化
####数据库初始化####
SQLInit.SQLInit(MySQLInfo)
##初始化已经拥有的资讯日期
DateACK_Init.ACK_Init(DateACK,MySQLInfo)
#print(DateACK)
##初始化默认的爬取日期####
ProcessInfo.set("待命")
ConsoleInfo.set("")
Start,End=DateCrawl_Init.DateCrawlInit(DateCrawl,DateACK,UserRuir[0])#在15天里，却没有爬取的日期
StartDate.set('开始日期:'+Start)
EndDate.set('结束日期:'+End)
KeyA.set('关键词A:'+'NULL')
KeyB.set('关键词B:'+'NULL')
Cycle.set('周期长度：'+'15天')
Sort.set('选择类型：'+'最热')
############################################################

###触发函数设计
def ToKeyWord():#关键词联系挖掘
    try:
        ToUpDateDate(False)#不设置直接自定义
    except:
        pass
    else:
        #def InfoSelect(DateCrawl,DictDate,path,DateSE,MySQLInfo,KEYA, KEYB, ANALYTYPE, SORTTYPE):
        UserRuir[1]=ANALYTYPE.DICT#关键词
        if KeyAIn.get()=='' or KeyBIn.get()=='':
            ConsoleInfo.set("关键词非法")
            return
        else:
            SD=StartDate.get().split(':')[1]
            ED=EndDate.get().split(':')[1]
            A=KeyAIn.get().encode('utf-8')
            B=KeyBIn.get().encode('utf-8')
            KeyA.set('关键词A:%s'%(A))
            KeyB.set('关键词B:%s'%(B))
            try:
                #def InfoSelect(DateCrawl,DictDate,path,DateSE,MySQLInfo,KEYA, KEYB, ANALYTYPE, SORTTYPE):
                InfoSelect(DateCrawl,DictDate,
                                    path=FILEPATH,DateSE=[SD,ED],MySQLInfo=MySQLInfo, 
                                    KEYA=A, KEYB=B,
                                    ANALYTYPE=UserRuir[1], SORTTYPE=UserRuir[2])
            except Exception as e:
                ConsoleInfo.set(e)
def ToDateWord():#词频分析
    try:
        ToUpDateDate(False)#不设置直接自定义
    except:
        pass
    else:
        #def InfoSelect(DateCrawl,DictDate,path,DateSE,MySQLInfo,KEYA, KEYB, ANALYTYPE, SORTTYPE):
        UserRuir[1]=ANALYTYPE.DATE#日期查询
        try:
            SD=StartDate.get().split(':')[1]
            ED=EndDate.get().split(':')[1]
            A=KeyAIn.get().encode('utf-8')
            B=KeyBIn.get().encode('utf-8')
            InfoSelect(DateCrawl,DictDate,
                path=FILEPATH,DateSE=[SD,ED],MySQLInfo=MySQLInfo, 
                KEYA=A, KEYB=B,
                ANALYTYPE=UserRuir[1], SORTTYPE=UserRuir[2])
        except Exception as e:
            ConsoleInfo.set(e)
def ToUpDateDate(flag=True):#指定时间
    Flag=(StartDateIn.get()=='' or EndDateIn.get()=='' ) and flag
    if Flag:#空
        ConsoleInfo.set("日期非法")
        return
    else:#非空
        try:#日期有效
            Start,End=DateCrawl_Init.DateCrawlInit(DateCrawl,DateACK,UserRuir[0],StartDateIn.get(),EndDateIn.get())#在选定时间里，没有爬取的日期
            StartDate.set('开始日期:%s'%StartDateIn.get())
            EndDate.set('结束日期:%s'%EndDateIn.get())
            ProcessInfo.set("日期设置")
        except:#日期无效#初始化
            ConsoleInfo.set("日期非法采用周期长度")
            Start,End=DateCrawl_Init.DateCrawlInit(DateCrawl,DateACK,UserRuir[0])#在15天里，却没有爬取的日期
            StartDate.set('开始日期:'+Start)
            EndDate.set('结束日期:'+End)
            StartDateIn.set('')
            EndDateIn.set('')
# def ToShow():
#     if(DateCrawl):
#         InfoSelect.InfoSelect(DateCrawl)
#     #print(IKEYA)
#     #thread.start_new_thread(InfoAnalysis.InfoAnalysis,(IKeyA,IKeyB,IDate,IRequir,))   
#     Show.Show()
# def ToDown():
#     InfoSelect.InfoSelect(DateCrawl,DateAnnDict,FILEPATH,Date,MySQLInfo)
#     #def InfoSelect(DateCrawl,DictDate,path,Date,MySQLInfo):
#     #DictDate={}#每天对应一堆字符串 {日期：{标题：[词，词，词]，标题：[词，词，词]}}
#     #DateDict ###{日期：{词:词数,词:词数}}`
#     try:
#         flag=Show.Show(DisplayFrame,UserRuir)#图像展示需要交互信息和图表
#     except Exception as e:
#         print("错误类型,错误明细")
#         print(e.__class__.__name__,e)
#     else:
#         pass
def Exit():
    exit()
def CallCyCle():
    
    if CycleLenth.get()=="TINY":#=7#周
        UserRuir[0]=CYCLELENTH.TINY
        Cycle.set('周期长度：'+'7天')
    elif CycleLenth.get()=="SMALL":#=15#两周 默认
        UserRuir[0]=CYCLELENTH.SMALL
        Cycle.set('周期长度：'+'15天')
    elif CycleLenth.get()=="MEDIUM":#=30#一个月
        UserRuir[0]=CYCLELENTH.MEDIUM
        Cycle.set('周期长度：'+'30天')
    elif CycleLenth.get()=="LARGE":#=90#一个季度
        UserRuir[0]=CYCLELENTH.LARGE
        Cycle.set('周期长度：'+'90天')
    elif CycleLenth.get()=="HUGE":#=365#一年
        UserRuir[0]=CYCLELENTH.HUGE
        Cycle.set('周期长度：'+'365天')
    Start,End=DateCrawl_Init.DateCrawlInit(DateCrawl,DateACK,UserRuir[0])#在15天里，却没有爬取的日期
    StartDate.set('开始日期:'+Start)
    EndDate.set('结束日期:'+End)
    ProcessInfo.set("周期设置")
def CallSort():
    if SortType.get()=="HOT":#=1#最热 默认
        UserRuir[2]=SORTTYPE.HOT
        Sort.set('选择类型：'+'最热')
    elif SortType.get()=="DENSITY":#2#最快
        UserRuir[2]=SORTTYPE.DENSITY
        Sort.set('选择类型：'+'最快')
    ProcessInfo.set("排序设置")

###按钮控件设置
ButtonDate=Tk.Button(InputFrame,text="词频分析",command=ToDateWord, background = BUTTONBACKGROUNDCOLOR)##日期挖掘ToShow():
ButtonDate.place(relx=0.55,rely=0.05,relwidth=0.2,relheight=0.10)
ButtonDict=Tk.Button(InputFrame,text="关键词联系挖掘",command=ToKeyWord, background = BUTTONBACKGROUNDCOLOR)##关键词挖掘ToDown():
ButtonDict.place(relx=0.55,rely=0.35,relwidth=0.2,relheight=0.10)
ButtonDict=Tk.Button(InputFrame,text="指定时间",command=ToUpDateDate, background = BUTTONBACKGROUNDCOLOR)##关键词挖掘ToDown():
ButtonDict.place(relx=0.78,rely=0.05,relwidth=0.2,relheight=0.10)
ButtonExit=Tk.Button(InputFrame,text="退出",command=Exit)##安全退出Exit():
ButtonExit.place(relx=0.9,rely=0.94,relwidth=0.1,relheight=0.06)

#group = Tk.LabelFrame(InputFrame, text='周期设置：').place(relx=0.55,rely=0.60,relwidth=0.1,relheight=0.24)
Tk.Label(InputFrame,textvariable=Cycle,background=LABELBACKGROUNDCOLOR).place(relx=0.55,rely=0.50,relwidth=0.15,relheight=0.10)
Tk.Radiobutton(InputFrame,text="一周",value="TINY",variable=CycleLenth,command=CallCyCle,indicatoron=False, background = BUTTONBACKGROUNDCOLOR).place(relx=0.55,rely=0.60,relwidth=0.15,relheight=0.06)
Tk.Radiobutton(InputFrame,text="两周",value="SMALL",variable=CycleLenth,command=CallCyCle,indicatoron=False, background = BUTTONBACKGROUNDCOLOR).place(relx=0.55,rely=0.66,relwidth=0.15,relheight=0.06)
Tk.Radiobutton(InputFrame,text="一月",value="MEDIUM",variable=CycleLenth,command=CallCyCle,indicatoron=False, background = BUTTONBACKGROUNDCOLOR).place(relx=0.55,rely=0.72,relwidth=0.15,relheight=0.06)
Tk.Radiobutton(InputFrame,text="一季",value="LARGE",variable=CycleLenth,command=CallCyCle,indicatoron=False, background = BUTTONBACKGROUNDCOLOR).place(relx=0.55,rely=0.78,relwidth=0.15,relheight=0.06)
Tk.Radiobutton(InputFrame,text="一年",value="HUGE",variable=CycleLenth,command=CallCyCle,indicatoron=False, background = BUTTONBACKGROUNDCOLOR).place(relx=0.55,rely=0.84,relwidth=0.15,relheight=0.06)
Tk.Label(InputFrame,textvariable=Sort,background=LABELBACKGROUNDCOLOR).place(relx=0.7,rely=0.50,relwidth=0.15,relheight=0.10)
Tk.Radiobutton(InputFrame,text="最热",value="HOT",variable=SortType,command=CallSort,indicatoron=False, background = BUTTONBACKGROUNDCOLOR).place(relx=0.7,rely=0.60,relwidth=0.15,relheight=0.15)
Tk.Radiobutton(InputFrame,text="最快",value="DENSITY",variable=SortType,command=CallSort,indicatoron=False, background = BUTTONBACKGROUNDCOLOR).place(relx=0.7,rely=0.75,relwidth=0.15,relheight=0.15)
###


###交互信息设置完毕，进入交互状态
## update
#  detail description  刷新页面信息        
def update():#刷新页面信息  
    #print(UserRuir)
    pass
    root.after(100000, update)   # 这里的单位为毫秒
## run
#  detail description  暂无，复位功能
def run():
    pass

root.mainloop()    
