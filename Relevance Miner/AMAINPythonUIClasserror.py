# -*- coding: utf-8 -*-
##
#  @file "InfoAnalysis.py"  
#  @brief "Matlab数据绘图"
#  @brief "对收集到的词频信息，并根据制表要求进行指定卷积等数据操作，最后生成图表"      
#  @author "Bernard "  
#  @date "2019-5-11"       
import Tkinter as Tk
import  Crawl
import  Show
##  INPUTBACKGROUNDCOLOR输入区背景色
##  DISPLAYBACKGROUNDCOLOR展示区背景色
INPUTBACKGROUNDCOLOR="Wheat"
DISPLAYBACKGROUNDCOLOR="LawnGreen"
class MainControl(Tk.Tk):
    
    def __init__(self):
        Tk.Tk(self).__init__()
        ###设置交互窗基础信息
        self.title('关联挖掘')                   #窗口名
        self.configure(background='white')          #窗口背景色           
        self.geometry('1366x768')                   # 设置窗口大小
        self.resizable(width=True, height=True)    # 设置窗口宽度可变，高度可变
        ###
        
        ###划区
        ##  InputFrame 输入控制放置区
        ##  DisplayFrame 展示插件放置区
        self.InputFrame=Tk.Frame(self,background=INPUTBACKGROUNDCOLOR)#声明
        self.InputFrame.place(relx=0.0,rely=0.0,relwidth=0.5,relheight=1)#放置
        self.DisplayFrame=Tk.Frame(self,background=DISPLAYBACKGROUNDCOLOR)#声明
        self.DisplayFrame.place(relx=0.5,rely=0.0,relwidth=0.5,relheight=1)#放置
        ###

        ###标签变量
        ##  ProcessInfo#精度信息 type=Tkinter.StringVar()
        self.ProcessInfo=Tk.StringVar()#精度信息
        ###

        ###控件设置
        self.ButtonDate=Tk.Button(InputFrame,text="词频分析",command=ToShow)##日期挖掘
        self.ButtonDate.place(relx=0.5,rely=0.5,relwidth=0.1,relheight=0.1)
        self.ButtonDict=Tk.Button(InputFrame,text="关键词联系挖掘",command=ToShow)##关键词挖掘
        self.ButtonDict.place(relx=0.4,rely=0.5,relwidth=0.1,relheight=0.1)
        ###
        self.run()
        self.update()
        self.mainloop()    
    ## update
    #  detail description  刷新页面信息        
    def update(self):
        self.after(100, self.update)   # 这里的单位为毫秒
    ## run
    #  detail description  暂无，复位功能
    def run(self):
        pass
    ###触发设计
    def ToShow(self):
        Show.Show()
    
MAINCONTORL=MainControl()
