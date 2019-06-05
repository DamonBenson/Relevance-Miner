# -*- coding: utf-8 -*-
##
#  @file "InfoAnalysis.py"  
#  @brief "Matlab数据绘图"
#  @brief "对收集到的词频信息，并根据制表要求进行指定卷积等数据操作，最后生成图表"      
#  @author "Bernard "  
#  @date "2019-5-11"
@@@@@@该函数重写，这是旧版本       
import time
import matlab.engine
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
## InfoAnalysis
#  detail description  本模块主函数，绘制输入两个关键词词频信息与日期直接的关系图
#  并根据内部功能绘制两个词频之间的系统关系，绘制出冲激响应图表
#  制表要求会影响日期轴的周期等。返回以上3个表Figure(matplotlib)
#  @type    KeyA:[[string,string,int]]
#  @param   KeyA:第一个关键词的词频信息[日期，对应的字，对应的字词数]
#  @type    KeyB:[[string,string,int]]
#  @param   KeyB:第二个关键词的词频信息[日期，对应的字，对应的字词数]
#  @type    Date:string
#  @param   Date:查询日期
#  @type    Requir:short
#  @param   Requir:制表要求
#  @return
#  @type    FigureA:matplotlib.figure.Figure
#  @retval  FigureA:第一个关键词与日期直接的关系图
#  @type    FigureB:matplotlib.figure.Figure
#  @retval  FigureB:第二个关键词与日期直接的关系图
#  @type    FigureAB:matplotlib.figure.Figure
#  @retval  FigureAB:两个词频之间的系统关系图
#  @note
def InfoAnalysis(KeyA,KeyB,Date,Requir,DateAnnDict):
    
    KeyAName=KeyA[0][1]#第一个关键词叫什么
    KeyBName=KeyB[0][1]#第二个关键词叫什么
    KeyADate=[]#第一个关键词的哪天统计结果
    KeyANum=[]#第一个关键词的某天统计结果
    KeyBDate=[]#第二个关键词的哪天统计结果
    KeyBNum=[]#第二个关键词的某天统计结果
    ###提取词频数组的信息
    while(KeyA):#KeyA中还有元素
        TempKey=KeyA.pop()#获取一个词频元素[string,string,int]
        KeyADate.append(TempKey[0])
        KeyANum.append(TempKey[2])
    while(KeyB):
        TempKey=KeyB.pop()#获取一个词频元素[string,string,int]
        KeyBDate.append(KeyB[0])
        KeyBNum.append(KeyB[2])
    ###
    
    datelenth=eng.HN(KeyBDate,2,nargout=4)
    
eng = matlab.engine.start_matlab()
'''
figure1 = Figure(figsize=(5,4), dpi=100)
a1 = figure1.add_subplot(111)
sys_e = []
x = []
total_e = []
for N in range (50,501,50):
    atom = ideal_gas(N,500,1000,1)
    sys_e.append(500-atom['demon']['e'])
    x.append(N)
    total_e.append(500)
a1.plot(x,total_e)
a1.plot(x,sys_e)
a1.convert_xunits('J')
a1.set_xlabel("N")
a1.set_ylabel("Energy")
a1.set_title('Energy')
canvas = FigureCanvasTkAgg(figure1,root)
canvas.get_tk_widget().pack(anchor = E , expand=1)
canvas.draw()
'''
'''
a,b,c,d=eng.HN(1,2,nargout=4)
print(a)
print(b)
print(c)
print(d)
print "Press Any Key to Exit"
raw_input();###暂停
eng.quit()
print "Bye-Bye"
##
#  detail description  本模块主函数，绘制输入两个关键词词频信息与日期直接的关系图
#  并根据内部功能绘制两个词频之间的系统关系，绘制出冲激响应图表
#  制表要求会影响日期轴的周期等。返回以上3个表Figure(matplotlib)
#  @param KeyA  第一个关键词的词频信息
#  @param KeyB  第二个关键词的词频信息
#  @param Date  查询日期
#  @param Requir    制表要求
#  @return   
#  @retval  FigureDraw 第一个关键词与日期直接的关系图
#  @retval  FigureDraw 第二个关键词与日期直接的关系图
#  @retval  FigureDraw 两个词频之间的系统关系图
#  @note
def 
'''