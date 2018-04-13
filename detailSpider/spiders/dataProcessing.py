# # coding=utf-8
# import codecs
# from bs4 import BeautifulSoup
# HTML = 'D:\MyCode\Python\sihuo\content.html'
# TXT = 'text.txt'
#
# # demo.html就是主页面
# def getUrl():
#     soup = BeautifulSoup(open(HTML), "lxml")
#     div = soup.find_all(attrs={'class': '_fhph4u'})
#     urls = []
#     s = set('')
#     for i in div:
#         for j in i.find_all('a'):
#             # j['href']里面有重复的，我放到set里去重，然后再放到list
#             url = "https://www.airbnb.com" + j['href']
#             print url
#             s.add(url)
#     while len(s):
#         urls.append(s.pop())
#     return urls
# if __name__ == '__main__':
#     s = getUrl()
#     with codecs.open(TXT,"w",encoding="utf-8") as f:
#         for i in s:
#             f.write(i)