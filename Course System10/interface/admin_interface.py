# 管理员接口
from db import models


# 管理员注册接口
def admin_register_interface(username, password):
    admin_obj = models.Admin.select(username)

    if not admin_obj:
        admin_obj = models.Admin(username, password)
        admin_obj.save()

        return True, f'管理员 [{username}] 注册成功！'

    return False, f'管理员 [{username}] 已存在！'


def create_school_interface(school_name, school_addr, admin_user):
    school_obj = models.School.select(school_name)

    if not school_obj:
        admin_obj = models.Admin.select(admin_user)
        admin_obj.create_school(school_name, school_addr)

        return True, f'管理员 [{admin_user}] 创建 [{school_name}] 学校成功！'

    return False, f'学校 [{school_name}] 已存在！'


def create_course_interface(school_name, course_name, admin_user, pried, price):
    school_obj = models.School.select(school_name)
    course_list = school_obj.school_course_list

    if course_name not in course_list:
        admin_obj = models.Admin.select(admin_user)
        admin_obj.create_course(school_obj, course_name, pried, price)

        return True, f'创建 [{course_name}] 课程成功，绑定给了 [{school_name}] 学校！'

    return False, f'课程 [{course_name}] 已存在不可重复创建！'


def create_teacher_interface(teacher_name, admin_user, teacher_pwd='123'):
    teacher_obj = models.Teacher.select(teacher_name)

    if not teacher_obj:
        admin_obj = models.Admin.select(admin_user)
        admin_obj.create_teacher(teacher_name, teacher_pwd)

        return True, f'创建 [{teacher_name}] 老师成功！'

    return False, f'老师 [{teacher_name}] 已存在！'


def pay_balance_interface(stu_name, money, admin_user):
    student_obj = models.Student.select(stu_name)

    if student_obj:
        money = int(money)
        admin_obj = models.Admin.select(admin_user)
        admin_obj.pay_balance(student_obj, money)

        return True, f'学生 [{stu_name}] 充值 [{money}] 元学费成功！'

    return False, f'学生 [{stu_name}] 不存在！'
