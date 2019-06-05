# -*- coding: utf-8 -*-
##
#  @file "InfoPreprocessor.py"  
#  @brief "资讯信息处理"
#  @brief "按日期批量处理pdf进而查出查出资讯时间，标题,词频信息"      
#  @author "Bernard "  
#  @date "2019-5-30" 
import json
import os
import re
import P2S#"pdf按日期文件夹寻找并转为txt"pdfTotxt(filepath,outpath)
import WordSplit#"分词以统计"  WordSplit(txtstr)
import WordCount#统计一天的词语词频，而每个公告的词频为1故不做统计，数据库不做相应的改动
import KeyWordSelect#"查出资讯时间，标题"  可惜当前没有
#pdfTotxt(u'F:\\pdf\\2013\\000001_平安银行_2013年年度报告_2562.pdf',u'test.txt')
##读文本txt
def text_read(filename):
    # Try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        file = open(filename,'r')
    except IOError:
        error = []
        return error
    content = file.read()
    file.close()#关闭文件是该函数存在的意义
    return content#str
##按日期格式文件名，读取每天PDF，并存在相应文件夹
def InfoPreprocessor(fileDir,DateCrawled):
    fileDir=fileDir.decode('utf-8')
   # fileDir = unicode(fileDir,'utf-8')
   ###更新公告转为字符串，再由字符串到词语，词语以中文的逗号分隔
    DateAnncDict={}#每天对应一堆字符串 {日期：{标题：[词，词，词]，标题：[词，词，词]}}
    for Date in DateCrawled:#每天文件夹隔开
        DateAnncDict[Date]={}#以当天日期为键，内容为以标题为键的字典
        DateDir=Date[0:4]+'-'+Date[4:6]+'-'+Date[6:8]
        DateFilesDir=fileDir+'\\'+DateDir#还原绝对地址
        files=os.listdir(DateFilesDir)#读取全部pdf
        TarDir=DateFilesDir+'txt'#输出文件夹
        if not os.path.exists(TarDir):#创建输出文件夹
            os.mkdir(TarDir)
        replace=re.compile(r'\.pdf',re.I)
        replacetxt=re.compile(r'\.txt',re.I)
        ####pdf转化
        print("转化字符串中，"+DateFilesDir.encode('utf-8'))
        TotalFile=len(files)
        NowFile=1
        try:
            for file in files:#遍历当天pdf
                ###转pdf
                filePath=DateFilesDir+'\\'+file
                outPath=TarDir+'\\'+re.sub(replace,'',file)+'.txt'#输出文件名
                P2S.pdfTotxt(filePath,outPath)#转txt
                NowFile=NowFile+1
                print('%d/%d'%(NowFile,TotalFile))
        except Exception, e:
            print "Exception:%s",e
       
        ###字符串读取
        print(u'更新字典') 
        TarDirfile=os.listdir(TarDir)#读取全部txt 
        #print(TarDir)  
        #print(TarDirfile)
        TotalFile=len(TarDirfile)
        NowFile=1    
        for txtfile in TarDirfile:
            outPath=TarDir+'\\'+txtfile
            AnncString=text_read(outPath)#读出字符串，防止中途bug，转换和读字符串分开
            #过河拆桥放在P2S中
            # os.remove(filePath)
            ###分词
            WordSplitResult=WordSplit.WordSplit(AnncString)#获取字词列表
            ##字典赋值
            #每日公告字典获得
            # AnncWord=WordSplitResult.split(',')
            AnncWord=WordSplitResult
            ###寻找关键信息当前没有任何功能很蠢
            AnncDate,AnncName=KeyWordSelect.KeyWordSelect(AnncString)
            ###
            AnncName=re.sub(replacetxt,'',txtfile)#标题
            AnncDate=Date#日期 没用因为键是日期
            AnncSingleData={AnncName:AnncWord}#每个公告需要存在字典的内容 标题：[词，词，词]
            DateAnncDict[Date].update(AnncSingleData)
            #DateAnncDict[Date].append(WordSplitResult)
            ##每日公告赋值完成
            ###计数
            NowFile=NowFile+1
            print('%d/%d'%(NowFile,TotalFile))
            ###
            
        
    ###此时DateAnncDict已经准备完成
    try:
        del AnncSingleData#释放寄存字典
    except UnboundLocalError :
        pass
    ###由{日期：{标题：[词，词，词]，标题：[词，词，词]}}
    ###获得
    ###{日期：{词:词数,词:词数}}
    ###每日字典更新
    DateDict=WordCount.WordCount(DateAnncDict)
    return  DateDict,DateAnncDict
    ###
            

    
# ##测试
# if __name__ == "__main__":
#     str="没门"
#     #str=str.encode('utf-8')
#     # DateAnncDict={'20170101':str}
#     DateCrawled=['20190531']#要处理的日期
#     DIR="爬取文件"#路径
#     DateDict,DateAnncDict=InfoPreprocessor(DIR,DateCrawled)
#     for DateAnnc in DateAnncDict['20190531']:
#         # for Annc in DateAnnc.keys():
#         #     print Annc
#         # str=json.dumps(DateAnncDict, ensure_ascii=False)
#         # print (str)
#         # str=json.dumps(DateDict, ensure_ascii=False)
#         # print (str)
        
#         for i in DateAnncDict:#日期键
#             print(i)
#             for j in DateAnncDict[i]:#标题键
#                 print (j)
#                 for k in DateAnncDict[i][j]:#词
#                     print(k)
#         for i in DateDict:#日期键
#             print(i)
#             for j in DateDict[i]:#词键
#                 print (j)
#                 print(DateDict[i][j])

#         #print (Annc.keys().encode('utf-8'))
#         #json.dumps(DateDict['20190531'], ensure_ascii=False, encoding='UTF-8')
#     #str=json.dumps(DateAnncDict, ensure_ascii=False)
#     #print (str)
#    # DateAnncDict.update(DateAnncDictUpdate)
#     #释放更新单元
#     #print (json.dumps(DateAnncDict, ensure_ascii=False, encoding='UTF-8'))非法
