# -*- coding: utf-8 -*-
##
#  @file "P2S.py"  
#  @brief "资讯公告转txt"
#  @brief "pdf按日期文件夹寻找并转为txt"      
#  @author "Bernard "  
#  @date "2019-5-30"  
import os
import re
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams

#将一个pdf转换成txt
def pdfTotxt(filepath,outpath):
    try:
        fp = file(filepath, 'rb')
        outfp=file(outpath,'w')
        #创建一个PDF资源管理器对象来存储共享资源
        caching = False#不缓存
        rsrcmgr = PDFResourceManager(caching = False)
        # 创建一个PDF设备对象
        laparams = LAParams()
        device = TextConverter(rsrcmgr, outfp, codec='utf-8', laparams=laparams,imagewriter=None)
        #创建一个PDF解析器对象
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, pagenos = set(),maxpages=0,
                                      password='',caching=False, check_extractable=True):
            page.rotate = page.rotate % 360
            interpreter.process_page(page)
        #关闭输入流
        fp.close()
        #关闭输出流
        device.close()
        outfp.flush()
        outfp.close()
        os.remove(filepath)
    except Exception as e:
        print ("Exception:%s"%e)
        try:
            #关闭输入流
            fp.close()
            #关闭输出流
            device.close()
            outfp.flush()
            outfp.close()
        except:
            pass
       
        os.remove(filepath)
        print('Removd!!!')
        print(filepath)

# #***后面是用来调试接口********************************************************************
# import WordSplit
# import json
# #pdfTotxt(u'F:\\pdf\\2013\\000001_平安银行_2013年年度报告_2562.pdf',u'test.txt')
# ##读文本txt
# def text_read(filename):
#     # Try to read a txt file and return a list.Return [] if there was a mistake.
#     try:
#         file = open(filename,'r')
#     except IOError:
#         error = []
#         return error
#     content = file.read()
#     file.close()#关闭文件是该函数存在的意义
#     return content#str
# ##按日期格式文件名，读取每天PDF，并存在相应文件夹
# def DefinedpdfTotxt(fileDir,DateCrawled):
#    # fileDir = unicode(fileDir,'utf-8')
#    #更新公告转为字符串
#     DateDictStr={}#每天对应一堆字符串
#     for Date in DateCrawled:#每天文件夹隔开
#         DateDictStr[Date]=[]#以当天日期为键
#         DateFilesDir=fileDir+'\\'+Date#还原绝对地址
#         files=os.listdir(DateFilesDir)#读取全部pdf
#         TarDir=DateFilesDir+'txt'#输出文件夹
#         if not os.path.exists(TarDir):#创建输出文件夹
#             os.mkdir(TarDir)
#         replace=re.compile(r'\.pdf',re.I)
#         print("转化字符串中，"+DateFilesDir.encode('utf-8'))
#         for file in files:#遍历当天pdf
#             filePath=DateFilesDir+'\\'+file
#             outPath=TarDir+'\\'+re.sub(replace,'',file)+'.txt'#输出文件名
#             pdfTotxt(filePath,outPath)#转txt
#             AnncString=text_read(outPath)#读出字符串，防止中途bug，转换和读字符串分开
#             WordSplitResult=WordSplit.WordSplit(AnncString)
#             DateDictStr[Date].append(WordSplitResult)
#             print (outPath.encode('utf-8'))
#     return DateDictStr
#     #return DateDictStr     
    
# ##测试
# if __name__ == "__main__":
#     str="没门"
#     #str=str.encode('utf-8')
#     DateDictStr={'20170101':str}
#     DateCrawled=['20190531', '20190601']#要处理的日期
#     DIR=u"F:\\2019sp\\Py\\源码\\手动爬取"#路径
#     DateDictStrUpdate=DefinedpdfTotxt(DIR,DateCrawled)
#     DateDictStr.update(DateDictStrUpdate)
#     del DateDictStrUpdate
#     #print (json.dumps(DateDictStr, ensure_ascii=False, encoding='UTF-8'))非法
#     str=json.dumps(DateDictStr, ensure_ascii=False)
#     print (str)
