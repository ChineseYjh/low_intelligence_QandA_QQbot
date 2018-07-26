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
import sys
import io
import I_wonder

robot_card = "QQ小水"
group_members_path = lambda group_nick : '.qqbot-tmp/plugins/members_of_group_{}.txt'.format(group_nick)
group_chat_log_path = lambda group_nick : '.qqbot-tmp/plugins/chat_log_of_group_{}.txt'.format(group_nick)
#my_group_name = "tests"
log_time_obj = datetime.datetime(2018,7,25)
#sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码

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
                    #写入昵称，一行一个，注意这里解码到记事本应该用gbk
                    f.write(member.nick.encode('utf-8').decode('gbk','ignore'))
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
                        f.write(member.nick.encode('utf-8').decode('gbk','ignore'))
                        f.write('\n')
                print("check-new done with true.")
                return True
            else:
                print("check-new done with false.")
                return False
    except:
        print("Exception arises.")
        raise
        pass

def I_wonder_that(question):
    """
    组合使用I_wonder模块中的函数
    @para: str
    @return: str
    """
    zhidao_list = ['如何','怎么样']
    baike_list = ['谁是','是谁', '什么是','是什么']
    answer = None
    for word in zhidao_list:
        if(word in question):
            answer = I_wonder.I_wonder_zhidao(question)
            if(answer == None):
                answer = I_wonder.I_wonder_baike(question)
                if(answer == None):
                    print("wonder done.")
                    return "嘤嘤嘤，小水也不知道呀/快哭了...你可以进这个群（825357177）问问~祝你好运咯！"
                print("wonder done.")
                return answer
            print("wonder done.")
            return answer
    for word in baike_list:
        if(word in question):
            answer = I_wonder.I_wonder_baike(question)
            if(answer == None):
                answer = I_wonder.I_wonder_zhidao(question)
                if(answer == None):
                    print("wonder done.")
                    return "emmm，这个小水怎么知道啊/快哭了...你可以进这个群（825357177）问问~祝你好运咯！"
                print("wonder done.")
                return answer
            print("wonder done.")
            return answer
    answer = I_wonder.I_wonder_zhidao(question)
    if(answer == None):
        answer = I_wonder.I_wonder_baike(question)
        if(answer == None):
            print("wonder done.")
            return "嘤..这种问题小水也回答不来/快哭了...你可以进这个群（825357177）问问~祝你好运咯！"
        print("wonder done.")
        return answer
    print("wonder done.")
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
#    """当有人说话时，查看该群是否有新人"""
#    if (check_new_member(bot,contact)):
#        say_hello = """
#        欢迎欢迎~快爆出你靓丽的照片吧，可以获得群主特献的头衔哦！
#        群相册里你也能看到小伙伴们精美的照骗~/可爱
#        另外，福建的小伙伴请加群150066099；有数学问题想问或者热爱数学
#        的小伙伴请加群825357177~北邮将带给你无限的精彩！/可爱
#        """
#        time.sleep(random.uniform(0.3,2.3))
#        bot.SendTo(contact,say_hello)
    """当content内有@机器人的信息时，进行相应的反应"""
    #这里@后面可能是昵称也可能是群名片
    #所以要获取自己在本群的群名片，但是这个比较复杂先不实现了
    if ("[@ME]" in content or ("@"+robot_card) in content):
        time.sleep(random.uniform(0.7,2.3))
        #发送信息
        #print(os.path.abspath("."))
        if("[@ME]" in content):
            question = content.replace("[@ME]",'')
        elif(("@" + robot_card) in content):
            question = content.replace("@"+robot_card,'')
        response = I_wonder_that(question)
        bot.SendTo(contact,response)
        #记录日志
        with open(group_chat_log_path(contact.nick),'a') as f:
            f.write('['+str(log_time_obj.today())+']\n')
            f.write(member.nick + ': ' + content + '\n')
            f.write('ROBOT: ' + response + '\n')
            f.write("""
===============================================================\n
                    """)
    #当content内没有@机器人的信息时，在一定概率下进行自我推销
    elif (random.randint(1,100) == 9):
        #1/100的可能性
        time.sleep(random.uniform(1.3,3.3))
        default_content = """
        想和我聊天吗？我还在升级对话系统，完成后就能完全回来陪你们啦！
        来~预热一下，@我来问问题，看看小水能答对几个诶嘿嘿嘿/可爱
        （小水不和群里的小伙伴抢红包哈~）
        """
        bot.SendTo(contact,default_content)
        
