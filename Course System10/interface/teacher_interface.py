from db import models


def check_course_interface(teacher_user):
    teacher_obj = models.Teacher.select(teacher_user)
    course_list = teacher_obj.teacher_course_list

    return course_list


def choose_course_interface(course_name, teacher_user):
    teacher_obj = models.Teacher.select(teacher_user)
    course_list = teacher_obj.teacher_course_list

    if course_name not in course_list:
        teacher_obj.choose_course(course_name)

        return True, f'选择 [{course_name}] 课程成功！'

    return False, f'课程 [{course_name}] 已存在教授课程列表中！'


def check_stu_from_course_interface(course_name):
    course_obj = models.Course.select(course_name)
    student_list = course_obj.student_list
    return student_list


def chang_score_interface(course_name, student_name, score, teacher_user):
    teacher_obj = models.Teacher.select(teacher_user)
    teacher_obj.change_score(course_name, student_name, score)
    return True, f'为学生 [{student_name}] 打分成功！'
