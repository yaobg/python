"""
定义jinja2 环境变量
"""
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse
from jinja2 import Environment


def register_jinja2_env(**options):
    # 创建环境对象
    env = Environment(**options)
    # 自定义语法：{{static('静态文件的相对路径')}} {{url('路由命名空间')}}
    env.globals.update({
        'static': staticfiles_storage.url,  # staticfiles_storage 获取静态文件的前缀
        'url': reverse,  # 反向解析
    })
    # 返回环境对象
    return env
