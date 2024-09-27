from ronglian_sms_sdk import SmsSDK

accId = '2c94811c9035ff9f0192321b28a566a6'
accToken = '38f1211eeeab45ce9e2f8e5750b02fc9'
appId = '2c94811c9035ff9f0192321b2a1d66ad'


def send_sms(mobile, code):
    sdk = SmsSDK(accId, accToken, appId)
    tid = '1'
    sdk.sendMessage(tid, mobile, (code, 60))


class CCP(object):
    """短信单例设计模式"""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not hasattr(CCP, "_instance"):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
        return cls._instance
