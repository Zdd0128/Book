# 用户视图层  主视图


from core import admin
from core import student
from core import teacher

func_dic = {
    '1': ('1.管理功能', admin.admin_view),
    '2': ('2.学生功能', student.student_view),
    '3': ('3.老师功能', teacher.teacher_view),
}


def run():
    while True:
        print('管理员功能'.center(21,'='))
        for key in func_dic:
            print(func_dic[key][0].center(20,' '))
        print('end'.center(24,'='))

        choice = input('请输入功能编号:').strip()

        if choice == 'q':
            break

        if choice in func_dic:
            func_dic[choice][1]()

        else:
            print('请输入正确编号！')
