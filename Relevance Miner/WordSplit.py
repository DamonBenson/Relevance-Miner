# -*- coding: utf-8 -*-
##
#  @file "WordSplit.py"  
#  @brief "词频统计"
#  @brief "分词以统计"      
#  @author "Bernard "  
#  @date "2019-5-30" 
import jieba
import jieba.posseg as pseg
import jieba.analyse
import re

def WordSplit(AnncString,SplitWay=1):
    #print(u"分词开始")
    WordSplitResult=[]#初始化返回列表
    if SplitWay==1:
        Resultlen= len(AnncString)/50#每50个词取一个关键词
        if Resultlen<=0:
            Resultlen=1
        if Resultlen>=200:
            Resultlen=200
        tag=jieba.analyse.extract_tags(AnncString,Resultlen)#关键词获取
    else:
        taggen=jieba.cut(AnncString, HMM=True)#精准模式
        tag=[]
        for i in taggen:
            tag.append(i)
    # str=(',').join(tag)
    # print(str.encode('utf-8'))
    zhPattern = re.compile(u'[\u4e00-\u9fa5]' ) 
    Total=len(tag)
    index=0
    while(index<Total):
        SelWord=tag[index]
        flag=zhPattern.search(SelWord)
        if flag:#是中文本
            if len(tag[index])<2:
                tag.pop(index)
                Total=Total-1
            else:
                index=index+1
        else:#不是
            #print(tag.pop(index))
            tag.pop(index)
            Total=Total-1
    #distinct化
    Result=[]
    for i in tag:
        if i not in Result:
            Result.append(i)
    WordSplitResult=Result
    return WordSplitResult
    #print(u"分词结束")

##按日期格式文件名，读取每天PDF，并存在相应文件夹
##测试
if __name__ == "__main__":
    #txtpath=u'F:\\2019sp\\Py\\源码\\手动爬取\\20190531txt\\惠城环保.txt'#指定文件
    #txtpath=u'F:\\2019sp\\Py\\源码\\手动爬取\\20190531txt\\惠城环保.txt'#指定文件
    txtpath=u'F:\\2019sp\\Py\\源码\\手动爬取\\20190601txt\\哈工智能.txt'#指定文件
    txt=open(txtpath,'r')
    txtstr=txt.read()
    tag=WordSplit(txtstr,0)
    print(tag)
