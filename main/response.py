#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from main import wechat, app
from .models import User


def wechat_response(data):
    """微信消息处理回复"""
    wechat.parse_data(data)
    message = wechat.get_message()
    # 用户信息写入数据库
    user = User(openid=message.source)
    user.save()
    # 默认回复微信信息
    response = 'success'
    if message.type == 'text':
        # 替换全角空格为半角空格
        message.content = message.content.replace(u'　', ' ')
        # 清除行首空格
        message.content = message.content.lstrip()
        # TODO 繁体转换或增加繁体关键字判断
        commands = {
            u'^\?|^？': all_command,
            u'^留言|^客服': leave_a_message,
            u'雷达': weather_radar,
            u'电话': phone_number,
            u'^公交|^公车': bus_routes,
            u'放假|校历': academic_calendar,
            u'合作': contact_us,
            u'明信片': postcard,
            u'游戏': html5_games,
            u'成绩': developing,
            u'新闻': developing,
            u'天气': developing,
            u'陪聊': developing,
            u'四六级': developing,
            u'图书馆': developing,
            u'签到': developing,
            u'音乐': developing,
            u'论坛': developing,
            u'快递': developing,
            u'更新菜单': update_menu_setting
        }
        # 找出指令对应的回复
        command_match = False
        for key_word in commands:
            if re.match(key_word, message.content):
                response = commands[key_word]()
                command_match = True
                break
        # 缺省回复
        if not command_match:
            response = command_not_found()
    elif message.type == 'click':
        commands = {
            'phone_number': phone_number,
            'score': developing,
            'express': developing,
            'search_books': developing,
            'chat_robot': developing,
            'sign': developing,
            'music': developing,
            'weather': developing
        }
        response = commands[message.key]()
    elif message.type == 'subscribe':
        response = subscribe()
    else:
        pass

    return response


def developing():
    """维护公告"""
    return wechat.response_text('该功能维护中，过两天再来吧')


def update_menu_setting():
    """更新自定义菜单"""
    try:
        wechat.create_menu(app.config['MENU_SETTING'])
    except Exception, e:
        return wechat.response_text(e)
    else:
        return wechat.response_text('Done!')


def postcard():
    """明信片查询"""
    return wechat.response_text(app.config['POSTCARD_TEXT'])


def html5_games():
    """HTML5游戏"""
    return wechat.response_text(app.config['HTML5_GAMES_TEXT'])


def contact_us():
    """合作信息"""
    content = app.config['CONTACT_US_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)


def academic_calendar():
    """校历"""
    return wechat.response_news(app.config['ACADEMIC_CALENDAR_NEWS'])


def bus_routes():
    """公交信息"""
    return wechat.response_news(app.config['BUS_ROUTES_NEWS'])


def weather_radar():
    """气象雷达动态图"""
    content = app.config['WEATHER_RADAR_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)


def leave_a_message():
    """留言提示"""
    content = app.config['LEAVE_A_MESSAGE_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)


def command_not_found():
    """非关键词回复"""
    content = app.config['COMMAND_NOT_FOUND_TEXT'] + app.config['COMMAND_TEXT']
    return wechat.response_text(content)


def all_command():
    """回复全部指令"""
    content = app.config['COMMAND_TEXT']
    return wechat.response_text(content)


def subscribe():
    """回复订阅事件"""
    content = app.config['WELCOME_TEXT'] + app.config['COMMAND_TEXT']
    return wechat.response_text(content)


def phone_number():
    """回复电话号码"""
    content = app.config['PHONE_NUMBER_TEXT'] + app.config['HELP_TEXT']
    return wechat.response_text(content)
