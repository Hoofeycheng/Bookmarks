import redis
from django.conf import settings
from django.shortcuts import render,redirect,reverse,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.http import JsonResponse,HttpResponse
from django.contrib import messages

from images.forms import ImageCreateForm
from images.models import Image
from actions.utils import create_action

# Create your views here.

r = redis.StrictRedis(host=settings.REDIS_HOST,port=settings.REDIS_PORT,db=settings.REDIS_DB)

@login_required
def image_create(request):
    if request.method == "POST":
        #表单提交
        form = ImageCreateForm(request.POST)
        if form.is_valid():
            #表单通过认证
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            #将当前用户附加到数据对象上
            new_image.user = request.user
            new_image.save()
            create_action(request.user,"添加了图片",new_image)
            messages.success(request,"图片添加成功！")
            return redirect(reverse("dashboard"))
    else:
        form = ImageCreateForm(request.GET)
    data = {
        "section":"images",
        "form":form,
    }
    return render(request,"images/create.html",data)

def image_list(request):
    """图片列表"""
    image_object_list = Image.objects.all()
    paginator = Paginator(image_object_list,4)
    page = request.GET.get("page")
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        #如果页数不是一个整数，返回第一页
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        #如果是不存在的页数，显示最后一页
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,"images/list_ajax.html",{"section":"images","images":images})
    data = {
        "section": "images",
        "images":images,
    }
    return render(request,"images/image_list.html",data)

def image_detail(request,id,slug):
    """
    展示图片
    :param request:
    :param id:       图片的id
    :param slug:     图片的slug字段
    :return:
    """
    image = get_object_or_404(Image,id=id,slug=slug)
    #浏览数+1
    #incr(),函数自动+1，设置amount=10自动默认+10
    total_views = r.incr("image:{}:views".format(image.id),amount=11)
    #在有序集合中，把image.id的分数增加1
    r.zincrby("image_ranking",1,image.id)
    data = {
        "section":"images",
        "image_obj":image,
        "total_views":total_views,
    }
    return render(request,"images/detail.html",data)

@login_required
def image_like(request):
    image_id = request.POST.get("id",None)
    action = request.POST.get("action",None)

    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == "like":
                image.user_like.add(request.user)
                create_action(request.user,"喜欢了图片",image)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({"status":"ok"})
        except Exception as e:
            print(e)
            pass
    return JsonResponse({"status":"error"})

@login_required
def image_ranking(request):
    #获取排名前十的图片列表
    image_ranking = r.zrange("image_ranking",0,-1,desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    #取出排名前十的图片排序
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    #按照每个image对象的id在image_ranking_ids中的排序，对查询结果组成的列表进行排序
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    data = {
        "section": "ranking",
        "most_viewed":most_viewed,
    }
    return render(request,"images/ranking.html",data)





