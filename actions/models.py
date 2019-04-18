from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

#一个关联到ContentType模型的ForeignKey，这会用来反映与外键所在的模型关联的具体模型
#一个存储具体的模型主键的字段，通常采用PositiveIntegerField字段，已匹配主键自增字段，这个字段用于从相关的具体模型中确定一个对象
class Action(models.Model):
    #进行行为的主体
    user = models.ForeignKey(User,related_name="actions",on_delete=models.CASCADE)
    #行为的动词，描述用户进行了什么行为
    verb = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType,blank=True,related_name="target_obj",on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True,blank=True,db_index=True)
    #GenericForeignKey,通过组合target_ct，target_id来得到具体的实例对象
    target = GenericForeignKey("target_ct","target_id")
    created = models.DateTimeField(auto_now_add=True,db_index=True)

    class Meta:
        ordering = ("-created",)

#Django的contenttypes框架，使用这个模型，我们目前只能记录行为的主体和动作，即用户A关注了。。或者用户上传了。。。还缺少行为的目标，我们还需要一个外键关联到用户操作的具体对象上，这样才能展示类似用户A关注了用户B的行为流。但是ForeignKey已经不能满足需求，目标对象可以是一个已经存在的任意一个模型对象








