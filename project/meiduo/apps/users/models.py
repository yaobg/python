from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

# Create your models here.
class User(AbstractUser):
    """
    自定义用户模型列
    :param AbstractUser:
    :return:
    """
    mobile = models.CharField(max_length=11, unique=True, verbose_name='手机号')

    # 元类
    class Meta:
        db_table = 'tb_users'  # 自定义表名
        verbose_name = '用户'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
