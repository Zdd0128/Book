from db import models
from conf import settings
import os


def get_login(username, password, user_type):
    if user_type == 'admin':
        obj = models.Admin.select(username)

    elif user_type == 'student':
        obj = models.Student.select(username)

    elif user_type == 'teacher':
        obj = models.Teacher.select(username)

    else:
        return False, '未知身份禁止登录！'

    if obj:
        if password == obj.pwd:
            return True, f'用户 [{username}] 登陆成功！'

        return False, '密码错误！'

    return False, f'用户 [{username}] 不存在！'


def get_all_school():
    school = os.path.join(
        settings.DB_PATH, 'school'
    )
    if os.path.exists(school):
        school_list = os.listdir(school)
        return school_list


def get_all_course():
    course = os.path.join(
        settings.DB_PATH, 'course'
    )
    if os.path.exists(course):
        all_course_list = os.listdir(course)
        return all_course_list
