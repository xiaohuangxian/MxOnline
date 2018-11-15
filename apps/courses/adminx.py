# encoding:utf-8
__author__ = 'Fioman'
__date__ = '2018/11/15 19:35'

from .models import *
import xadmin


# Course的admin管理器
class CourseAdmin(object):
    # 显示字段列表
    list_display = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students']
    # 搜索字段
    search_fields = ['name', 'desc', 'detail', 'degree', 'students']
    # 过滤筛选
    list_filter = ['name', 'desc', 'detail', 'degree', 'learn_time', 'students']


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    # __name代表使用外键中name字段
    list_filter = ['course__name', 'name', 'add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download', 'add_time']
    search_fields = ['course', 'name', 'download']
    list_filter = ['course__name', 'name', 'download', 'add_time']


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(ResourceCourse, CourseResourceAdmin)
