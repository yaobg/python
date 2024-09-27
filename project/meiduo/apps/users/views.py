import os
import re

from django.contrib.auth import login, authenticate
from django.db import DatabaseError
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

from users import models
from apps.utils.response_code import RET


# Create your views here.

class UsernameCountView(View):
    """
    判断用户名是否重复注册
    """

    def get(self, request, username):
        count = models.User.objects.filter(username=username).count()
        return JsonResponse({'code': RET.OK, 'count': count})


class MobileCountView(View):
    """
    判断用户名是否重复注册
    """

    def get(self, request, mobile):
        count = models.User.objects.filter(mobile=mobile).count()
        return JsonResponse({'code': RET.OK, 'count': count})


class LoginView(View):
    """
    用户登录
    """

    def get(self, request):
        """提供注册页面"""
        return render(request, 'login.html')

    def post(self, request):
        """实现登录逻辑"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        remembered = request.POST.get('remembered')
        if not all([username, password]):
            return JsonResponse({'code': RET.PARAMERR, 'errmsg': '缺少必传参数'})
        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({'code': RET.PARAMERR, 'errmsg': '用户名格式错误'})
        if not re.match(r'^[0-9A-Za-z]{6,20}$', password):
            return JsonResponse({'code': RET.PARAMERR, 'errmsg': '密码格式错误'})
        # 认证用户

        user = authenticate(request, username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'account_errmsg': '用户名或密码错误'})
        login(request, user)
        # 状态保持
        # 默认是session保存，可以修改为cookie保存
        # request.session.set_expiry(60)
        # 登录成功，重定向到首页
        if remembered == 'on':
            request.session.set_expiry(None)
        response = redirect(reverse('contents:index'))
        response.set_cookie('username', username, max_age=14 * 24 * 3600)
        return response


class RegisterView(View):
    """
    用户注册
    """

    def get(self, request):
        """提供注册页面"""
        return render(request, 'register.html')

    @csrf_exempt
    def post(self, request):
        """实现注册逻辑"""
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        allow = request.POST.get('allow')
        # all 会去校验列表中的元素是否为空，只要有一个为空，则返回False
        if not all([username, password, password2, mobile, allow]):
            return JsonResponse({'code': 400, 'errmsg': '缺少必传参数'})

        if not re.match(r'^[a-zA-Z0-9_-]{5,20}$', username):
            return JsonResponse({'code': 400, 'errmsg': '用户名格式错误'})
        if not re.match(r'^1[3-9]\d{9}$', mobile):
            return JsonResponse({'code': 400, 'errmsg': '手机号格式错误'})

        if password != password2:
            return JsonResponse({'code': 400, 'errmsg': '两次密码不一致'})
        if allow != 'on':
            return JsonResponse({'code': 400, 'errmsg': '请勾选用户协议'})
        try:
            user = models.User.objects.create_user(username=username, password=password, mobile=mobile)
        except DatabaseError:
            return render(request, 'register.html', {'register_errmsg': '注册失败'})

        login(request, user)
        # 动态解析路由
        return redirect(reverse('contents:index'))

    # 登录
