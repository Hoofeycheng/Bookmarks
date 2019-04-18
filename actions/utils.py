#-*- coding:utf-8 -*-
#程序员：Hoofey Cheng
#座右铭：人生苦短 我用Python!
#时间：2019/1/24 10:26
#文件名称：utils.py
#使用的IDE:PyCharm

import datetime
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from actions.models import Action

def create_action(user,verb,target=None):
    #检查一分钟内的相同动作
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(user_id=user.id,verb=verb,created__gte=last_minute)

    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(target_ct=target_ct,target_id=target.id)

    if not similar_actions:
    #一分钟内找不到相似的记录
        action = Action(user=user,verb=verb,target=target)
        action.save()




