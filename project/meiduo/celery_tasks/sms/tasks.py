# 定义任务函数
from celery_tasks.main import celery_app
from celery_tasks.sms.yuntongxun import sms


# 使用装饰器装饰异步任务
@celery_app.task(name='send_sms_code')
def send_sms_code(mobile, code):
    """

    :param mobile: 手机号
    :param code: 验证码
    :return: 成功 0 失败 -1
    """
    return sms.send_sms(mobile, code)
