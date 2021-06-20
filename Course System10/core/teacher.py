# 老师视图
from interface import common_interface
from interface import teacher_interface
from lib import common

teacher_info = {'user': None}


# 登录
def login():
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()

        flag, msg = common_interface.get_login(
            username, password, user_type='teacher'
        )
        if flag:
            print(msg)
            teacher_info['user'] = username
            break
        else:
            print(msg)


# 查看教授课程
@common.login_auth('teacher')
def check_course():
    while True:
        course_list = teacher_interface.check_course_interface(
            teacher_info.get('user')
        )
        if not course_list:
            print('当前没有教授课程，请先添加！')
            break
        for index, course_name in enumerate(course_list):
            print('教授课程编号：%s   教授课程名称：%s' % (index, course_name))
        break


# 选择教授课程
@common.login_auth('teacher')
def choose_course():
    while True:
        all_course_list = common_interface.get_all_course()

        if not all_course_list:
            print('当前没有任何课程，请联系管理员创建！')
            break

        for index, course_name in enumerate(all_course_list):
            print('课程编号：%s   课程名称：%s' % (index, course_name))

        choice = input('请输入编号选择课程：').strip()

        if not choice.isdigit():
            print('请输入数字！')
            continue

        choice = int(choice)

        if choice not in range(len(all_course_list)):
            print('请输入正确编号！')
            continue

        course_name = all_course_list[choice]

        flag, msg = teacher_interface.choose_course_interface(
            course_name, teacher_info.get('user')
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 查看课程下的学生
@common.login_auth('teacher')
def check_stu_from_course():
    while True:
        course_list = teacher_interface.check_course_interface(
            teacher_info.get('user')
        )
        if not course_list:
            print('当前没有教授课程，请先添加！')
            break

        for index, course_name in enumerate(course_list):
            print('课程编号：%s   课程名称：%s' % (index, course_name))

        choice = input('请输入编号选择课程：').strip()

        if not choice.isdigit():
            print('请输入数字！')
            continue

        choice = int(choice)

        if choice not in range(len(course_list)):
            print('请输入正确编号！')
            continue

        course_name = course_list[choice]

        student_list = teacher_interface.check_stu_from_course_interface(
            course_name
        )
        if not student_list:
            print('当前课程没有学生选择！')
            break
        for number, student_name in enumerate(student_list):
            print('学生编号：%s    学生姓名：%s' % (number, student_name))
        break


# 修改学生分数
@common.login_auth('teacher')
def change_score_from_student():
    while True:
        course_list = teacher_interface.check_course_interface(
            teacher_info.get('user')
        )
        if not course_list:
            print('当前暂无教授可程，不可查看学生！')
            break
        for index1, course_name in enumerate(course_list):
            print('课程编号：%s   课程名称：%s' % (index1, course_name))

        choice = input('请输入课程编号：').strip()

        if not choice.isdigit():
            print('请输入数字！')
            continue

        choice = int(choice)

        if choice not in range(len(course_list)):
            print('请输入正确编号！')
            continue

        course_name = course_list[choice]

        student_list = teacher_interface.check_stu_from_course_interface(course_name)
        if not student_list:
            print('当前课程下没有学生！')
            continue
        for index2, student_name in enumerate(student_list):
            print('学生编号：%s   学生名称：%s' % (index2, student_name))

        stu_choice = input('请输入学生编号为其打分：').strip()

        if not stu_choice.isdigit():
            print('请输入数字！')
            continue

        stu_choice = int(stu_choice)

        if stu_choice not in range(len(student_list)):
            print('请输入正确编号！')
            continue

        student_name = student_list[stu_choice]

        score = input('请输入成绩：').strip()

        flag, msg = teacher_interface.chang_score_interface(
            course_name, student_name, score, teacher_info.get('user')
        )
        if flag:
            print(msg)
            break


teacher_dic = {
    '1': ('1.老师登录功能', login),
    '2': ('2.查看教授课程', check_course),
    '3': ('3.选择教授课程', choose_course),
    '4': ('4.查看课程学生', check_stu_from_course),
    '5': ('5.修改学生分数', change_score_from_student),
}


def teacher_view():
    while True:
        print('老师功能'.center(21, '='))
        for key in teacher_dic:
            print(teacher_dic[key][0].center(20, ' '))
        print('end'.center(24, '='))

        choice = input('请输入功能编号:').strip()

        if choice == 'q':
            break

        if choice in teacher_dic:
            teacher_dic[choice][1]()

        else:
            print('请输入正确编号！')
