# celery 启动文件
from celery import Celery

# 创建Celery实例
celery_app = Celery('celery_tasks')
# 加载配置
celery_app.config_from_object('celery_tasks.config')
# 注销任务
celery_app.autodiscover_tasks(['celery_tasks.sms'])
