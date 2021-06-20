def login_auth(role):
    from core import admin
    from core import student
    from core import teacher
    def outer(func):
        def inner(*args, **kwargs):
            if role == 'admin':
                if admin.admin_info['user']:
                    res = func(*args, **kwargs)
                    return res
                else:
                    print('请先登录管理员用户！！！')

            elif role == 'student':
                if student.student_info['user']:
                    res = func(*args, **kwargs)
                    return res
                else:
                    print('请先登录学生用户！！！')

            elif role == 'teacher':
                if teacher.teacher_info['user']:
                    res = func(*args, **kwargs)
                    return res
                else:
                    print('请先登录老师用户！！！')

            else:
                print('未知身份不可使用本系统！')

        return inner

    return outer
