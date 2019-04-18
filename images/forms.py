#-*- coding:utf-8 -*-
#程序员：Hoofey Cheng
#座右铭：人生苦短 我用Python!
#时间：2019/1/21 14:11
#文件名称：forms.py
#使用的IDE:PyCharm

from django import forms
from urllib import request
from django.core.files.base import ContentFile
from django.utils.text import slugify
from images.models import Image

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        #展示在前端页面上的字段
        fields = ("title","url","description")

    #自定义验证器
    def clean_url(self):
        url = self.cleaned_data["url"]
        valid_ext = ["jpg","jpeg","png"]
        ext = url.split(".")[-1].lower()
        if ext not in valid_ext:
            raise forms.ValidationError("我们不支持您所提供的图片格式!")
        return url

    def save(self,commit=True):
        #先调用父类的save方法，使用现有的表单数据建立一个新的image数据对象，但是不保存
        #此处的save（）方法为模型的save方法
        image_obj = super(ImageCreateForm,self).save(commit=False)
        image_url = self.cleaned_data["url"]
        #将image，slug与扩展名拼接成新的文件名
        image_name = "{}.{}".format(slugify(image_obj.title),image_url.split(".")[-1].lower())
        #根据url下载图片
        response = request.urlopen(image_url)
        #使用urllib模块下载图片，然后使用image字段的save方法保存到media目录中
        #image字段的save方法的参数之一ContentFile是下载图片内容
        #使用（字段的save方法）save=False是防止直接将字段写入数据库
        image_obj.image.save(image_name,ContentFile(response.read()),save=False)

        #为了和原save（）方法行为保持一致,只有当commit=True的时候写入数据库
        if commit:
            image_obj.save()
        return image_obj









