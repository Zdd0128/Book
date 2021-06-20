from django import forms
from app01 import models


class Register(forms.Form):
    username = forms.CharField(max_length=6, min_length=3, label='用户名',
                               error_messages={
                                   'max_length': '用户名最大六位',
                                   'min_length': '用户名最少三位',
                                   'required': '用户名不能为空',
                               },
                               widget=forms.widgets.TextInput(attrs={'class': 'form-control'})
                               )

    password = forms.CharField(max_length=6, min_length=3, label='密码',
                               error_messages={
                                   'max_length': '密码最大六位',
                                   'min_length': '密码最少三位',
                                   'required': '密码不能为空',
                               },
                               widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                               )

    confirm_password = forms.CharField(label='确认密码',
                                       error_messages={
                                           'required': '确认密码不能为空',
                                       },
                                       widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'})
                                       )

    email = forms.EmailField(label='邮箱',
                             error_messages={
                                 'invalid': '邮箱格式不正确',
                                 'required': '邮箱不能为空',
                             },
                             widget=forms.widgets.EmailInput(attrs={'class': 'form-control'})
                             )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_obj = models.UserInfo.objects.filter(username=username).first()
        if user_obj:
            self.add_error('username', '该用户名已存在')

        return username

    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            self.add_error('confirm_password', '两次密码输入不一致')

        return self.cleaned_data
