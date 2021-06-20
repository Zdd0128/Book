# 管理员视图
from interface import admin_interface
from interface import common_interface
from lib import common

admin_info = {'user': None}


# 管理员注册
def register():
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()
        re_password = input('确认密码:').strip()

        if password == re_password:

            # 调用接口层，管理员注册接口
            flag, msg = admin_interface.admin_register_interface(
                username, password
            )
            if flag:
                print(msg)
                break
            else:
                print(msg)

        else:
            print('两次密码输入不一致！')


# 管理员登录
def login():
    while True:
        username = input('请输入用户名:').strip()
        password = input('请输入密码:').strip()

        flag, msg = common_interface.get_login(
            username, password, user_type='admin'
        )
        if flag:
            print(msg)
            admin_info['user'] = username
            break
        else:
            print(msg)


# 创建学校
@common.login_auth('admin')
def create_school():
    while True:
        school_name = input('请输入学校名称：').strip()
        school_addr = input('请输入学校地址：').strip()

        flag, msg = admin_interface.create_school_interface(
            school_name, school_addr, admin_info.get('user')
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 创建课程
@common.login_auth('admin')
def create_course():
    while True:
        school_list = common_interface.get_all_school()

        if not school_list:
            print('当前没有学校，请先创建学校！')
            break
        for index, school_name in enumerate(school_list):
            print('学校编号：%s   学校名称：%s' % (index, school_name))

        choice = input('请输入学校编号创建课程：').strip()

        if not choice.isdigit():
            print('请输入数字！')
            continue

        choice = int(choice)

        if choice not in range(len(school_list)):
            print('请输入正确编号！')
            continue

        school_name = school_list[choice]

        course_name = input('请输入课程名称进行创建：').strip()
        pried = input('请输入课程周期：').strip()
        price = input('请输入课程价格：').strip()

        flag, msg = admin_interface.create_course_interface(
            school_name, course_name, admin_info.get('user'), pried, price
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 创建讲师
@common.login_auth('admin')
def create_teacher():
    while True:
        teacher_name = input('请输入老师名称：').strip()

        flag, msg = admin_interface.create_teacher_interface(
            teacher_name, admin_info.get('user')
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)


# 学生充值学费
@common.login_auth('admin')
def pay_balance():
    while True:
        stu_name = input('请输入学生用户名：').strip()
        money = input('请输入充值金额：').strip()

        flag, msg = admin_interface.pay_balance_interface(
            stu_name, money, admin_info.get('user')
        )
        if flag:
            print(msg)
            break
        else:
            print(msg)


admin_dic = {
    '1': ('1.注册功能', register),
    '2': ('2.登录功能', login),
    '3': ('3.创建学校', create_school),
    '4': ('4.创建课程', create_course),
    '5': ('5.创建讲师', create_teacher),
    '6': ('6.学费充值', pay_balance),
}


def admin_view():
    while True:
        print('管理员功能'.center(21, '='))
        for key in admin_dic:
            print(admin_dic[key][0].center(20, ' '))
        print('end'.center(24, '='))

        choice = input('请输入功能编号:').strip()

        if choice == 'q':
            break

        if choice in admin_dic:
            admin_dic[choice][1]()

        else:
            print('请输入正确编号！')
