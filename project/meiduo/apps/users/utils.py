# 自定义认证后端，实现多方式登录
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

from users.models import User


class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户后端
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写认证方法
        :param request:
        :param username:
        :param password:
        :param kwargs:
        :return:
        """
        # 1. 根据用户名或手机号查询用户
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
        except User.DoesNotExist:
            return None
        # 2. 校验密码是否正确
        return user
