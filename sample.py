# -*- coding: utf-8 -*-
"""
Created on Thu Jun 28 17:36:46 2018

@author: ChineseYjh

E-mail: 877675495@qq.com
"""
import os
import time
import random
import datetime
import requests
import re
from bs4 import BeautifulSoup as bs
from bs4 import NavigableString as NavigableString

robot_card = "QQ小水"
group_members_path = lambda group_nick : '.qqbot-tmp/plugins/members_of_group_{}.txt'.format(group_nick)
group_chat_log_path = lambda group_nick : '.qqbot-tmp/plugins/chat_log_of_group_{}.txt'.format(group_nick)
#my_group_name = "18届咨询咨询群"
log_time_obj = datetime.datetime(2018,7,3)

def check_new_member(bot,contact):
    """
    查看是否有新成员，如果有则更新文件，否则不更新
    @para: QQBot, QContact
    @return: bool
    """
    #my_group = bot.List('group', contact.nick)[0]
    try:
        #更新群成员列表
        print("updating the member list...")
        if (not bot.Update(contact)):
            print("Update myGroup list error.")
        #查看是否有新成员在该列表中
        print("checking the new members...")
        group_members = bot.List(contact)
        if (not os.path.exists(group_members_path(contact.nick))):
            #第一次更新
            print("initiating the member file...")
            with open(group_members_path(contact.nick),'w') as f:
                for member in group_members:
                    #写入昵称，一行一个
                    f.write(member.nick)
                    f.write('\n')
        else:
            #进行比较
            print("comparing...")
            with open(group_members_path(contact.nick),'r') as f:
                for member in group_members:
                    isIn = False
                    for line in f.readlines():
                        if (member.nick == line.strip()):
                            isIn = True
                            break
                    f.seek(0,0)
                    if (not isIn):
                        #该member不在里面
                        break
            #如果有新成员，更新文件
            if(not isIn):
                print("rewriting...")
                with open(group_members_path(contact.nick),'w') as f:
                    for member in group_members:
                        #写入昵称，一行一个
                        f.write(member.nick)
                        f.write('\n')
                return True
            else:
                return False
    except:
        print("Exception arises.")
        raise
        pass

def I_wonder_baike(question):
    """
    利用百度百科查询question的百科，并返回内容
    @para: str
    @return: str
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
        return "嘤嘤嘤，小水也不知道/快哭了..."
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
        return "嘤嘤嘤，小水也不知道/快哭了..."

def I_wonder_zhidao(question):
    """
    利用百度知道查询question的百科，并返回内容
    @para: str
    @return: str
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
        return "嘤嘤嘤，小水也不知道/快哭了..."
    result_url_div = result_url_div[0]
    #print(result_url_div)
    result_url = result_url_div.attrs['href']
    r = requests.get(url=result_url, headers=headers)
    r.raise_for_status()
    r.encoding = r.apparent_encoding
    #print(r.text[:500])
    #抽取最佳答案
    print("extracting the best data...")
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
    
def onQQMessage(bot, contact, member, content):
# =============================================================================
#     """先确定是否是指定的群"""
#     if (contact.nick != my_group_name):
#         return
# =============================================================================

    """先确定是群，才回复"""
    if (member == None): 
        return
    """当有人说话时，查看该群是否有新人"""
    #if (check_new_member(bot,contact)):
    #    pass
    """当content内有@机器人的信息时，进行相应的反应"""
    #这里@后面可能是昵称也可能是群名片
    #所以要获取自己在本群的群名片，但是这个比较复杂先不实现了
    if ("[@ME]" in content or ("@"+robot_card) in content):
        time.sleep(random.uniform(0.7,2.3))
        #发送信息
        print(os.path.abspath("."))
        response = I_wonder_baike(content.replace("[@ME]",''))
        bot.SendTo(contact,response)
        #记录日志
        with open(group_chat_log_path(contact.nick),'a') as f:
            f.write('['+str(log_time_obj.today())+']\n')
            f.write(member.nick + ': ' + content + '\n')
            f.write('ROBOT: ' + response + '\n')
            f.write("""
===============================================================
                    """)
    #当content内没有@机器人的信息时，在一定概率下进行自我推销
    elif (random.randint(1,100) == 9):
        #1/10的可能性
        time.sleep(random.uniform(1.3,3.3))
        default_content = """
        想和我聊天吗？我还在升级对话系统，完成后就能完全回来陪你们啦！
        来~预热一下，@我来问问题，看看小水能答对几个诶嘿嘿嘿/可爱
        """
        bot.SendTo(contact,default_content)
        
