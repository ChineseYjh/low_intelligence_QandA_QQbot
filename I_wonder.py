# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 16:07:03 2018

@author: ChineseYjh

E-mail: 877675495@qq.com

Function: 该文件包括几种搜索问题的答案的简易爬虫
"""
import requests
import re
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString

def I_wonder_baike(question):
    """
    利用百度百科查询question的百科，并返回内容; 如果查不到，返回None
    @para: str
    @return: str or None
    """
    #查问题
    print("quering question...")
    baidu_baike_url = "https://baike.baidu.com/search/none?word="
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    r = requests.get(url=baidu_baike_url+question,headers=headers)
    r.raise_for_status()
    r.encoding = 'utf-8'
    soup = bs(r.text,'html.parser')
    #访问第一个链接
    print("visiting the answer...")
    result_url_div = soup.select("[class~=result-title]")
    if(result_url_div == []):
        return None
    result_url_div = result_url_div[0]
    result_url = result_url_div.attrs['href']
    if ("https://baike.baidu.com" not in result_url):
        result_url = "https://baike.baidu.com" + result_url
    r = requests.get(url=result_url,headers=headers)
    r.raise_for_status()
    r.encoding = 'utf-8'
    soup = bs(r.text,'html.parser')
    #抽取概要
    print("processing data...")
    try:
        div = soup.select("[class~=lemma-summary]")
        if (div == []):
            raise Exception("No answer")
        div = div[0]
        answer = ""
        tempnode = "None"
        for node in div.descendants:
            string = str(node.string)
            if (string == tempnode):
                pass
            elif (string == "None"):
                answer += '\n'
            elif (re.compile("\[[0-9]*]|\[[0-9]*-[0-9]*]").search(string)):
                pass
            else :
                if ("\xa0" in string):
                    string = string.replace("\xa0","")
                answer += string
                tempnode = string
        return answer
    except:
        return None


def I_wonder_zhidao(question):
    """
    利用百度知道查询question的百科，并返回内容;如果查不到，返回None
    @para: str
    @return: str or None
    """
    zhidao_url = "https://zhidao.baidu.com/search?ie=utf-8&word="
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
    print("quering the question...")
    r = requests.get(url=zhidao_url+question, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    soup = bs(r.text,'html.parser')
    #访问第一个非广告链接
    print("visiting the answer...")
    result_url_div = soup.select("#wgt-list > dl:nth-of-type(1) > dt > a")
    if(result_url_div == []):
        return None
    result_url_div = result_url_div[0]
    #print(result_url_div)
    result_url = result_url_div.attrs['href']
    r = requests.get(url=result_url, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    #print(r.text[:500])
    #抽取最佳答案
    print("extracting the best answer...")
    soup = bs(r.text, 'html.parser')
    #<div id='best-content-...'>
    tag = soup.find(name='div',attrs={'id':re.compile("best-content-[0-9]*")})
    #<pre>
    if(tag == None):
        tag = soup.find(name='pre',attrs={'id':re.compile("best-content-[0-9]*")})
        if(tag != None and tag.string != None):
            return str(tag.string)
    #<div id='answer-content-...'>
    if(tag == None):
        tag = soup.find(name='div',attrs={'id':re.compile("answer-content-[0-9]*")})
    #print(tag, tag.string, sep='\n')
    if(tag == None):
        return None
    answer = ""
    temp = ""#防止重复（在遍历时有的string一次在标签中一次本身被遍历）
    for p in tag.descendants:
        print(p)
        #<p>string</p>
        if(p.name == 'p' and p.string != None and temp != str(p.string)):
            temp = str(p.string)
            answer += temp
        #<a href="link">...</a>
        elif (p.name == 'a' and str(p.string) != "展开"):
            answer += ('\n' + p.attrs['href'] + '\n')
        #<span>string</span>
        elif(p.name == 'span' and p.string != None and temp != str(p.string)):
            temp = str(p.string)
            answer += temp
        #<a>展开<\a>
        elif(p.name == 'a' and str(p.string) == "展开"):
            print("need expand")
        #string
        elif(type(p) == NavigableString and str(p) != "展开全部" and temp != str(p)):
            temp = str(p)
            answer += temp
        #print("temp:", temp)
    #print("answer: ", answer)
    return answer



