# -*- coding: utf-8 -*-
##
#  @file "WordCount.py"  
#  @brief "词频统计"
#  @brief "词与词语数"      
#  @author "Bernard "  
#  @date "2019-5-30"  
###由{日期：{标题：[词，词，词]，标题：[词，词，词]}}
###获得
###{日期：{词:词数,词:词数}}
def WordCount(DateAnncDict):
    print(u"统计字符串中")
    DateDict={}#返回DATEINFO_DICT每日公告词典数据表要存的内容
    for Date in sorted(DateAnncDict,reverse=True):#降序排列
        DateDict[Date]={}#{日期：{词:词数,词:词数}} 选定天数
        #{标题：[词，词，词]，标题：[词，词，词]}对每个公告处理
        for Annc in DateAnncDict[Date].values():
            for DATE_DICT_WORD in Annc:#遍历所有词
                #print (DATE_DICT_WORD)
                if DATE_DICT_WORD not in DateDict[Date].keys():#之前没有加入该词
                    DateDict[Date].update({DATE_DICT_WORD:1})
                else:
                    DateDict[Date][DATE_DICT_WORD]=DateDict[Date][DATE_DICT_WORD]+1#之前有了自加一
    print(u"统计字符串结束")
    return DateDict
    