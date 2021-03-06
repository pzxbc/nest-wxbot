# -*- coding: utf-8 -*-


import itchat
import threading

itchat_lock = threading.RLock()
# 给外部用，名字更容易理解
bot_lock = itchat_lock
core = itchat


@itchat.msg_register(itchat.content.TEXT, isFriendChat=True)
def reply_friend_msg(msg):
    print(msg)
    return msg.text


@itchat.msg_register(itchat.content.TEXT, isGroupChat=True)
def reply_group_msg(msg):
    with itchat_lock:
        group = itchat.search_chatrooms(userName=msg['FromUserName'])
        if group and group['NickName'] == '开心玩～':
            print(type(msg), msg)
            return msg['Text']


# 调用接口
def send_friend_msg(msg, to_user):
    with itchat_lock:
        user = itchat.search_friends(nickName=to_user)
        if user:
            itchat.send_msg(msg, user[0]['UserName'])
            return True
    return False


def send_group_msg(msg, to_group):
    with itchat_lock:
        group = itchat.search_chatrooms(name=to_group)
        if group:
            itchat.send_msg(msg, group[0]['UserName'])
            return True
    return False


def get_receiver(to_chat):
    with itchat_lock:
        # 先找好友
        obj = itchat.search_friends(nickName=to_chat)
        if obj:
            return obj[0]['UserName']
        # 群组
        obj = itchat.search_chatrooms(name=to_chat)
        if obj:
            return obj[0]['UserName']
    return None


core.auto_login(hotReload=True, enableCmdQR=2)
core.run(debug=True, blockThread=False)
