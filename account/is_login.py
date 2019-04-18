#-*- coding:utf-8 -*-
#程序员：Hoofey Cheng
#座右铭：人生苦短 我用Python!
#时间：2019/1/21 9:07
#文件名称：is_login.py
#使用的IDE:PyCharm

"""
实现从浏览器过来的请求判断是否登录
"""
from django.http import HttpResponseRedirect

#自定义一个装饰器,检测用户是否为登录状态，代替自带的login_required检测
def is_login(func):
    def login_function(request,*args,**kwargs):
        if request.user.username:
            return func(request,*args,**kwargs)
        else:
            return HttpResponseRedirect("/account/login")
    return login_function









