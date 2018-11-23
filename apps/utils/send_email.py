# encoding:utf-8
from random import Random

from django.core.mail import send_mail # 导入Django自带的Email发送模块
from users.models import EmailVerifyRecord
from MxOnline.settings import EMAIL_FROM


__author__ = 'Fioman'
__date__ = '2018/11/23 10:36'

def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        str += chars[random.randint(0, length)]
    return str


# type 为发送邮箱干嘛的,这里用于激活
def send_register_email(email,send_ype="register"):
    # 发送之前保存到数据库,以便到时候查询链接是否存在

    # 实例化一个EmailVerifyRecord对象
    email_record = EmailVerifyRecord()
    # 生成随机的code放入到链接
    code = random_str(16)
    email_record.code = code
    email_record.email =email
    email_record.send_type = send_ype

    # 保存到数据库
    email_record.save()

    # 定义邮件的内容
    email_title = ""
    email_body = ""

    if send_ype == "register":
        email_title = "智学教育网 注册激活链接"
        email_body = "请点击下面的链接激活你的账号: http://127.0.0.1:8000/active/{0}".format(code)

        # 使用Django内置的函数完成邮件发送.四个参数:主题,邮件内容,从哪里发,接受者list
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])

        # 如果发送成功:
        if send_status:
            pass

