from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(User,related_name='images_created',on_delete=models.CASCADE)
    #图片名称
    title = models.CharField(max_length=200)
    #slug 图片的简称用户创建动态建立图片的url
    slug = models.CharField(max_length=200,blank=True)
    #image 图片文件字段，用于存放图片到媒体文件media中
    image = models.ImageField(upload_to="image/%Y")
    #存储网络图片地址到数据库中
    url = models.URLField()
    #图片的描述
    description = models.TextField(blank=True)
    #创建时间
    created = models.DateField(auto_now_add=True,db_index=True)
    #存储哪些用户喜欢该图片
    user_like = models.ManyToManyField(User,related_name="image_liked",blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = "images"

    def save(self,*args,**kwargs):
        """图片保存到数据库时，自动根据title字段生成slug字段的内容"""
        if not self.slug:
            self.slug = slugify(self.title)
        super(Image,self).save(*args,**kwargs)

    def get_absolute_url(self):
        return reverse("images:detail",args=[self.id,self.slug])


