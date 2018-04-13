# coding=utf-8
import codecs
import os
TXT = "D:\MyCode\Python\sihuo/text.txt"
def getUrl():
    urls = []
    path = 'url/'
    dir_list = os.listdir(path)
    for i in dir_list:
        with codecs.open(path + i,"r",encoding='utf-8')as file:
            for line in file.readlines():
                # if "select" in line:
                urls.append(line.strip('\n').split('?')[0])
    return urls