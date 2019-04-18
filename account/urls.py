#-*- coding:utf-8 -*-
#程序员：Hoofey Cheng
#座右铭：人生苦短 我用Python!
#时间：2019/1/17 16:06
#文件名称：urls.py
#使用的IDE:PyCharm

from django.urls import path
from account.views import user_login,dashboard,register,edit,user_list,user_detail,user_follow

from django.contrib.auth import views

urlpatterns = [
    # path('login/',user_login,name="login"),
    #注册页面
    path('register/',register,name='register'),
    #登录/退出页面
    path('login/',views.LoginView.as_view(),name="login"),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    #主页
    path('dashboard/',dashboard,name='dashboard'),
    #修改密码页面
    path('password_change/',views.PasswordChangeView.as_view(),name='password_change'),
    path('password_shange/done/',views.PasswordChangeDoneView.as_view(),name='password_change_done'),
    #重置密码，发送邮件页面
    path('password_reset/',views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    #邮件里面附带的重置密码链接页面
    path('reset/<uidb64>/<token>/',views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
    #编辑个人资料页面
    path('edit/',edit,name='edit'),
    #关注人的页面
    path('users/',user_list,name="user_list"),
    path('users/<username>/',user_detail,name="user_detail"),
    path('follow/',user_follow,name="follow"),
]


