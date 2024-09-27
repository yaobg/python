import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views import View
from django_redis import get_redis_connection

import celery_tasks.sms.tasks
from utils.captcha.captcha import captcha
from utils.response_code import RET
from utils.yuntongxun import sms
from verifications import constants


class SMSCodeView(View):
    """
    短信验证码
    """

    def get(self, request, mobile):
        # 获取参数
        image_code = request.GET.get('img_code')
        uuid = request.GET.get('uuid')
        if not all([image_code, uuid]):
            return HttpResponse('参数不齐全')
        redis_conn = get_redis_connection('default')
        image_code_key = 'ImageCode_' + uuid
        image_code_server = redis_conn.get(image_code_key)
        if image_code_server is None:
            return JsonResponse({'code': RET.IMAGECODERROR, 'errmsg': '图片验证码过期'})
        # 删除图形验证码
        redis_conn.delete(image_code_key)
        if image_code_server.decode().lower() != image_code.lower():
            return JsonResponse({'code': RET.IMAGECODERROR, 'errmsg': '图形验证码错误'})
        sms_code = random.randint(1000, 9999)
        redis_conn.setex('sms_%s' % mobile, constants.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 使用Celery异步发送短信
        celery_tasks.sms.tasks.send_sms_code.delay(mobile, sms_code)
        return JsonResponse({'code': RET.OK, 'errmsg': '短信发送成功'})


# Create your views here.


class ImageCodeView(View):

    def get(self, request, image_code_id):
        # 生成验证码
        name, text, image = captcha.generate_captcha()
        redis_conn = get_redis_connection('default')
        redis_conn.setex('ImageCode_' + image_code_id, 120, text)
        return HttpResponse(image, content_type='image/jpg')
