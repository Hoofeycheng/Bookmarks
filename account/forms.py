#-*- coding:utf-8 -*-
#程序员：Hoofey Cheng
#座右铭：人生苦短 我用Python!
#时间：2019/1/17 15:46
#文件名称：forms.py
#使用的IDE:PyCharm

from django import forms
from django.contrib.auth.models import User
from account.models import Profile

#widget=forms.PasswordInput，输入密码会隐藏，并显示为****
class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label="密码",widget=forms.PasswordInput)
    password2 = forms.CharField(label="确认密码",widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ("username","email")

    #clean_password2,该方法是一个验证器方法，会在调用is_vaild方法的时候执行
    #可以对任意字段采用clean_<field_name>方法创建一个验证器
    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("两次输入的密码不匹配！")
        return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("email",)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("birth_date","photo")

