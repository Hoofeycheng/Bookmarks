from django.shortcuts import render,HttpResponse,redirect,reverse,get_object_or_404
#authenticate,该方法接收request对象，username,password三个参数，到数据库中进行匹配。如果匹配成功，返回一个User数据对象，否则返回None.
from django.contrib.auth import authenticate,login
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse,HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User

from account.forms import LoginForm,UserRegistrationForm,UserEditForm,ProfileEditForm
from account.models import Profile,Contact
from account.is_login import is_login
from actions.utils import create_action
from actions.models import Action

# Create your views here.

#注册
def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            #建立新的数据对象，但是不写入数据库
            new_user = user_form.save(commit=False)
            #设置密码
            new_user.set_password(user_form.cleaned_data["password"])
            #保存User对象
            new_user.save()
            Profile.objects.create(user=new_user)
            create_action(new_user,"创建了新用户!")
            return render(request,"account/register_done.html",{"new_user":new_user})
    else:
        user_form = UserRegistrationForm()
    data = {
        "user_form":user_form,
    }
    return render(request,'account/register.html',data)

#登录
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        #这里执行is_valid()函数会调用forms文件中的clean_password2(self)验证器函数来验证表单信息是否存在
        if form.is_valid():
            cd = form.cleaned_data
            # authenticate,该方法接收request对象，username,password三个参数，到数据库中进行匹配。如果匹配成功，返回一个User数据对象，否则返回None.
            user = authenticate(request,username=cd["username"],password=cd["password"])
            if user is not None:
                if user.is_active:
                    #login()方法会在会话中设置用户信息
                    login(request,user)
                    return HttpResponse("登录成功！")
                else:
                    return HttpResponse("您的账户被禁用，请联系管理员解封！")
            else:
                return HttpResponse("登录失败！")
    else:
        form = LoginForm()
    data = {
        "form":form,
    }
    return render(request,"account/login.html",data)

#检测用户是否为登录状态
# @login_required
@is_login
def dashboard(request):
    #success，一个动作成功之后发送的消息
    #info     通知性的消息
    #warning  警告性质内容
    #error    错误信息
    #debug    给开发者展示，在生产环境中要移除
    # messages.error(request,"发生了一些错误！")
    #默认展示所有行为，不包含当前用户
    actions = Action.objects.exclude(user=request.user)
    #已关注用户的行为流
    #已关注的用户的id列表
    following = Contact.objects.filter(user_from=request.user)
    following_ids = [user_to.id for user_to in following]
    if following_ids:
        #如果当前用户有关注的用户，展示被关注用户的行为
        actions = actions.filter(user_id__in=following_ids)
    data = {
        "section":"dashboard",
        "actions":actions,
    }
    return render(request,'account/dashboard.html',data)

@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user,data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,data=request.POST,files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request,"个人信息编辑成功！")
            # return redirect(reverse("dashboard"))
        else:
            messages.error(request,"个人信息编辑失败啦！")
    else:
        #instance=,用于指定表单实例化为某个具体的数据对象
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    data = {
        "user_form":user_form,
        "profile_form":profile_form,
    }
    return render(request,"account/edit.html",data)

def user_list(request):
    users = User.objects.filter(is_active=True)
    data = {
        "section":"people",
        "users":users,
    }
    return render(request,"account/list.html",data)

@login_required
def user_detail(request,username):
    user = get_object_or_404(User,username=username,is_active=True)
    contacts = Contact.objects.filter(user_to=user)
    #关注列表
    followers = [contact.user_from for contact in contacts]
    total_followers = len(followers)
    data = {
        "section": "people",
        "user":user,
        "followers":followers,
        "total_followers":total_followers,
    }
    return render(request,"account/detail.html",data)

@login_required
def user_follow(request):
    user_id = request.POST.get("id",None)
    action = request.POST.get("action",None)

    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == "follow":
                Contact.objects.get_or_create(user_from=request.user,user_to=user)
                create_action(request.user,"关注了用户",user)
            else:
                Contact.objects.filter(user_from=request.user,user_to=user).delete()
            return JsonResponse({"status":"ok"})
        except Exception as e:
            print(e)
            pass
    return JsonResponse({"status":"error"})



