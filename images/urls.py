#-*- coding:utf-8 -*-
#程序员：Hoofey Cheng
#座右铭：人生苦短 我用Python!
#时间：2019/1/21 14:45
#文件名称：urls.py
#使用的IDE:PyCharm

from django.urls import path
from images.views import image_create,image_detail,image_list,image_like,image_ranking

app_name= "images"

urlpatterns = [
    path("list/",image_list,name="image_list"),
    path("create/",image_create,name="create"),
    path("detail/<int:id>/<slug:slug>/",image_detail,name="detail"),
    path("like/",image_like,name="like"),
    path("ranking/",image_ranking,name="ranking"),
]






