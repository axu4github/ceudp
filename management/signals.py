# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver
from management.models import User

__author__ = "axu"

"""
参考文档：
- https://docs.djangoproject.com/en/1.11/topics/signals/
"""


@receiver(post_save, sender=User)  # 发送给User
def instance_post_save(sender, instance, created, raw, *args, **kwargs):
    """
    保存后触发该方法，必须要在模型中复写post_save方法

    参考文档：
    - https://docs.djangoproject.com/en/1.11/ref/signals/#post-save
    """
    if hasattr(instance, "post_created") and created:
        instance.post_created()
