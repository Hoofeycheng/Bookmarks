#-*- coding:utf-8 -*-
#程序员：Hoofey Cheng
#座右铭：人生苦短 我用Python!
#时间：2019/1/21 10:50
#文件名称：authenticate.py
#使用的IDE:PyCharm

from django.contrib.auth.models import User

#每次使用authenticate函数时，Django会按照AUTHENTICATION_BACKENDS设置中列出的顺序，依次执行其中的验证后端进行验证，直到有一个验证返回成功为止，如果列表中的验证全部返回失败，这个用户就不会被验证失败

#自定义后端验证规则：一个验证后端必须是一个类，至少要有两个方法
#authenticate（）：参数request和用户验证信息，如果用户验证信息有效，必须返回一个user对象，否则就是None
#get_user:参数为用户id，返回一个user对象
class EmailAuthBackend:
    """使用电子邮件地址作为用户名验证登录"""
    def authenticate(self,request,username=None,password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self,user_id):
        try:
            return User.objects.get(id=user_id)
        except User.DoesNotExist:
            return None



