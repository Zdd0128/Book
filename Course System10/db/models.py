# 用于存放类
from db import db_handler


class SuperClass:
    @classmethod
    def select(cls, username):
        obj = db_handler.select_data(cls, username)
        return obj

    def save(self):
        db_handler.save_data(self)


class Admin(SuperClass):

    def __init__(self, username, password):
        self.user = username
        self.pwd = password

    def create_school(self, school_name, school_addr):
        school_obj = School(school_name, school_addr)
        school_obj.save()

    def create_course(self, school_obj, course_name, pried, price):
        school_obj.school_course_list.append(course_name)
        school_obj.save()

        course_obj = Course(course_name)
        course_obj.school = school_obj.user
        course_obj.course_dic[course_name] = [pried, price]
        course_obj.save()

    def create_teacher(self, teacher_name, teacher_pwd):
        teacher_obj = Teacher(teacher_name, teacher_pwd)
        teacher_obj.save()

    def pay_balance(self, student_obj, money):
        student_obj.balance = money
        student_obj.save()


class School(SuperClass):

    def __init__(self, school_name, school_addr):
        self.user = school_name
        self.addr = school_addr
        self.school_course_list = []


class Student(SuperClass):

    def __init__(self, username, password):
        self.user = username
        self.pwd = password
        self.balance = 0
        self.school = None
        self.student_course_dic = {}

    def choice_school(self, school_name):
        self.school = school_name
        self.save()

    def add_course(self, course_name):
        self.student_course_dic[course_name] = 0
        self.save()

        course_obj = Course.select(course_name)
        course_obj.student_list.append(self.user)
        course_obj.save()


class Course(SuperClass):

    def __init__(self, course_name):
        self.user = course_name
        self.school = None
        self.course_dic = {}
        self.student_list = []


class Teacher(SuperClass):

    def __init__(self, teacher_name, teacher_pwd):
        self.user = teacher_name
        self.pwd = teacher_pwd
        self.teacher_course_list = []

    def choose_course(self, course_name):
        self.teacher_course_list.append(course_name)
        self.save()

    def change_score(self, course_name, student_name, score):
        student_obj = Student.select(student_name)
        student_obj.student_course_dic[course_name] = score
        student_obj.save()
