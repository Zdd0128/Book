from db import models


def register_interface(username, password):
    student_obj = models.Student.select(username)

    if not student_obj:
        student_obj = models.Student(username, password)
        student_obj.save()

        return True, f'学生 [{username}] 注册成功！'

    return False, f'学生 [{username}] 已被注册！'


def choice_school_interface(school_name, student_user):
    student_obj = models.Student.select(student_user)
    school = student_obj.school

    if not school:
        student_obj.choice_school(school_name)

        return True, f'选择 [{school_name}] 学校成功！'

    return False, '当前已经选过学校，不可重复选择！'


def choice_course_interface(student_user):
    student_obj = models.Student.select(student_user)
    school = student_obj.school

    if school:
        school_obj = models.School.select(school)
        course_list = school_obj.school_course_list

        if course_list:
            return True, course_list

        return False, '当前学校没有课程，请联系管理员创建！'

    return False, '请先选择学校！'


def add_course_interface(course_name, student_user):
    student_obj = models.Student.select(student_user)
    course_dic = student_obj.student_course_dic

    course_obj = models.Course.select(course_name)
    price = course_obj.course_dic[course_name][1]
    price = int(price)

    if student_obj.balance >= price:
        student_obj.balance -= price

        if course_name not in course_dic:
            student_obj.add_course(course_name)

            return True, f'选择 [{course_name}] 课程成功！扣除学费 {price} 元！'

        return False, '当前课程已存在不可重复选择！'

    return False, '当前学费余额不足，不可选课，请联系管理员充值！'


def check_score_interface(student_user):
    student_obj = models.Student.select(student_user)
    course_dic = student_obj.student_course_dic

    if course_dic:
        return True, course_dic

    return False, '当前没有选择任何课程，请先选择！'


def check_course_interface(course_name):
    course_obj = models.Course.select(course_name)
    course_info = course_obj.course_dic
    school = course_obj.school

    if course_info:
        return course_info, school


def check_balance_interface(student_user):
    student_obj = models.Student.select(student_user)

    return True, student_obj.balance
