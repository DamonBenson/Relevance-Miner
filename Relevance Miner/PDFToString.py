# -*- coding: utf-8 -*-
##
#  @file "PDFToString.py"  
#  @brief "资讯公告转字符串"
#  @brief "pdf转字符串后顺便保存txt"      
#  @author "Bernard "  
#  @date "2019-5-30"  
import os
import re
import P2S
def text_read(filename):
    # Try to read a txt file and return a list.Return [] if there was a mistake.
    try:
        file = open(filename,'r')
    except IOError:
        error = []
        return error
    content = file.readlines()

    for i in range(len(content)):
        content[i] = content[i][:len(content[i])-1]

    file.close()
    return content
##测试
if __name__ == "__main__":
    DateCrawled=['20190531', '20190601']#要处理的日期
    Dir=u"F:\\2019sp\\Py\\源码\\手动爬取"#路径
    try:
        P2S.DefinedpdfTotxt(Dir,DateCrawled)
    except Exception, e:
        print "Exception:%s",e
    else:
        
        
            
        

