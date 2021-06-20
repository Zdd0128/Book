# 学生视图

from interface import common_interface
from interface import student_interface
from lib import common

student_info = {'user': None}


# 注册
def register():
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        re_password = input('请确认密码:').strip()

        if password == re_password:
            flag, msg = student_interface.register_interface(
                username, password
            )
            if flag:
                print(msg)
                break
            else:
                print(msg)

        else:
            print('两次密码输入不一致！')


# 登录
def login():
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()

        flag, msg = common_interface.get_login(
            username, password, user_type='student'
        )
        if flag:
            print(msg)
            student_info['user'] = username
            break
        else:
            print(msg)


# 选择校区
@common.login_auth('student')
def choice_school():
    while True:
        school_list = common_interface.get_all_school()
        if not school_list:
            print('当前没有学校，请联系管理员创建！')
            break
        for index, school_name in enumerate(school_list):
            print('学校编号：%s   学校名称：%s' % (index, school_name))

        choice = input('请输入编号选择学校：').strip()

        if not choice.isdigit():
            print('请输入数字！')
            continue

        choice = int(choice)

        if choice not in range(len(school_list)):
            print('请输入正确编号！')
            continue

        school_name = school_list[choice]

        flag, msg = student_interface.choice_school_interface(
            school_name, student_info.get('user')
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)
            break


# 查看课程
@common.login_auth('student')
def check_course():
    while True:
        course_list_all = common_interface.get_all_course()

        if not course_list_all:
            print(course_list_all)
            break
        for index, course_name in enumerate(course_list_all):
            print('课程编号：%s   课程名称：%s ' % (index, course_name))

        choice = input('请输入编号选择课程：').strip()

        if not choice.isdigit():
            print('请输入数字！')
            continue

        choice = int(choice)

        if choice not in range(len(course_list_all)):
            print('请输入正确编号！')
            continue

        course_name = course_list_all[choice]

        course_info, school = student_interface.check_course_interface(
            course_name
        )

        if not course_info:
            print('当前没有选择课程，请先选择！')
            break
        for course_name, pried_price in course_info.items():
            pried, price = pried_price
            print('课程名称(%s)：%s   课程周期：%s   课程价格：%s' % (school, course_name, pried, price))
        break


# 选择课程
@common.login_auth('student')
def choice_course():
    while True:
        flag, course_list = student_interface.choice_course_interface(
            student_info.get('user')
        )
        if not flag:
            print(course_list)
            break
        for index, course_name in enumerate(course_list):
            print('课程编号：%s   课程名称：%s ' % (index, course_name))

        choice = input('请输入编号选择课程：').strip()

        if not choice.isdigit():
            print('请输入数字！')
            continue

        choice = int(choice)

        if choice not in range(len(course_list)):
            print('请输入正确编号！')
            continue

        course_name = course_list[choice]

        flag, msg = student_interface.add_course_interface(
            course_name, student_info.get('user')
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)
            break


# 查看分数
@common.login_auth('student')
def check_score():
    while True:
        flag, score_dic = student_interface.check_score_interface(
            student_info.get('user')
        )
        if not flag:
            print(score_dic)
            break
        for course_name, score in score_dic.items():
            print('课程名称：%s   课程分数：%s' % (course_name, score))
        break


# 查看当前学费余额
@common.login_auth('student')
def check_balance():
    flag, balance = student_interface.check_balance_interface(
        student_info.get('user')
    )
    if flag:
        print('当前学费余额：%s 元' % balance)


student_dic = {
    '1': ('1.注册功能', register),
    '2': ('2.登录功能', login),
    '3': ('3.选择校区', choice_school),
    '4': ('4.查看课程', check_course),
    '5': ('5.选择课程', choice_course),
    '6': ('6.查看分数', check_score),
    '7': ('7.查看余额', check_balance),
}


def student_view():
    while True:
        print('学生功能'.center(22, '='))
        for key in student_dic:
            print(student_dic[key][0].center(20, ' '))
        print('end'.center(24, '='))

        choice = input('请输入功能编号:').strip()

        if choice == 'q':
            break

        if choice in student_dic:
            student_dic[choice][1]()

        else:
            print('请输入正确编号！')
