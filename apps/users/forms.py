# encoding:utf-8
__author__ = 'Fioman'
__date__ = '2018/11/16 16:59'

# 引入Django表单
from django import forms
# 引入验证码
from captcha.fields import CaptchaField


# 登录表单验证
class LoginForm(forms.Form):
    # 用户名密码不能为空
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)


# 注册类表单
class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)

    # 应用验证码
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


# 激活时验证码实现
class ActiveForm(forms.Form):
    # 激活时不对邮箱密码做验证
    # 应用验证码 自定义错误输出key必须与异常一样
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})
