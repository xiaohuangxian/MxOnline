# encoding:utf-8
__author__ = 'Fioman'
__date__ = '2018/11/15 16:37'

import xadmin

from .models import EmailVerifyRecord


# 创建admin的管理类,这里不再继承自admin,而是object
class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    search_fields = ['code', 'email', 'send_type'] # 时间不做搜索

xadmin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)
