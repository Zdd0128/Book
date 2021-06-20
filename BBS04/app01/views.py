from django.shortcuts import render, HttpResponse, redirect
from app01.myforms import Register
from django.http import JsonResponse
from app01 import models
from django.contrib import auth
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random

from utils.mypage import Pagination


# 注册
def register(request):
    form_obj = Register()
    if request.is_ajax():
        back_dic = {'code': 100}
        if request.method == 'POST':
            form_obj = Register(request.POST)
            if form_obj.is_valid():
                user_dic = form_obj.cleaned_data
                user_dic.pop('confirm_password')
                file_obj = request.FILES.get('avatar')
                if file_obj:
                    user_dic['avatar'] = file_obj

                models.UserInfo.objects.create_user(**user_dic)
                back_dic['msg'] = '注册成功'
                back_dic['url'] = '/app01/login/'
            else:
                back_dic['code'] = 101
                back_dic['msg'] = form_obj.errors

        return JsonResponse(back_dic)
    return render(request, 'register.html', locals())


# 登录功能
def login(request):
    if request.is_ajax():
        back_dic = {'code': 100}
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            code = request.POST.get('code')
            code_s = request.session.get('code')

            if not username:
                back_dic['code'] = 101
                back_dic['msg'] = '用户名不能为空'
                return JsonResponse(back_dic)

            if not password:
                back_dic['code'] = 101
                back_dic['msg'] = '密码不能为空'
                return JsonResponse(back_dic)

            if not code:
                back_dic['code'] = 101
                back_dic['msg'] = '验证码不能为空'
                return JsonResponse(back_dic)

            user_obj = models.UserInfo.objects.filter(username=username).first()
            if user_obj:
                if code.upper() == code_s.upper():
                    if auth.authenticate(request, username=username, password=password):

                        back_dic['msg'] = '登陆成功'
                        url = request.GET.get('next')
                        if url:
                            back_dic['url'] = url
                        else:
                            back_dic['url'] = '/app01/'
                        auth.login(request, user_obj)

                    else:
                        back_dic['code'] = 102
                        back_dic['msg'] = '用户名或密码错误'
                else:
                    back_dic['code'] = 103
                    back_dic['msg'] = '验证码不正确'
            else:
                back_dic['code'] = 104
                back_dic['msg'] = '当前用户不存在'

        return JsonResponse(back_dic)

    return render(request, 'login.html')


# 退出登录
def logout(request):
    auth.logout(request)

    return redirect('home_view')


# 随机背景色
def get_random():
    return random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)


# 随机验证码
def random_num(request):
    img_obj = Image.new('RGB', (220, 35), get_random())
    img_draw = ImageDraw.ImageDraw(img_obj)
    img_font = ImageFont.truetype('static/font/111.ttf', 35)

    code = ''
    for i in range(5):
        random_int = str(random.randint(0, 9))
        random_upper = chr(random.randint(65, 90))
        random_lower = chr(random.randint(97, 122))
        tmp = random.choice([random_int, random_upper, random_lower])
        img_draw.text((45 * i + 10, 1), tmp, get_random(), img_font)
        code += tmp

    request.session['code'] = code

    io_obj = BytesIO()
    img_obj.save(io_obj, 'png')

    return HttpResponse(io_obj.getvalue())


# 修改密码
def set_password(request):
    if request.is_ajax():
        back_dic = {'code': 100}
        if request.method == 'POST':
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('new_password')
            re_password = request.POST.get('re_password')

            if not old_password:
                back_dic['code'] = 101
                back_dic['msg'] = '原密码不能为空'
                return JsonResponse(back_dic)

            if not new_password:
                back_dic['code'] = 101
                back_dic['msg'] = '新密码不能为空'
                return JsonResponse(back_dic)

            if not re_password:
                back_dic['code'] = 101
                back_dic['msg'] = '确认密码不能为空'
                return JsonResponse(back_dic)

            if request.user.is_authenticated():
                if request.user.check_password(old_password):
                    if new_password == re_password:
                        request.user.set_password(new_password)
                        request.user.save()

                        back_dic['msg'] = '密码修改成功,请重新登录'
                        back_dic['url'] = '/app01/login/'

                    else:
                        back_dic['code'] = 102
                        back_dic['msg'] = '新密码两次输入不一致'
                else:
                    back_dic['code'] = 103
                    back_dic['msg'] = '原密码错误'

            else:
                back_dic['code'] = 104
                back_dic['msg'] = '请先登录'

        return JsonResponse(back_dic)


# home主页
def home(request):
    form_obj = Register()
    article_list = models.Article.objects.all()
    page_obj = Pagination(request.GET.get('page', 1), article_list.count(), per_page_num=4, pager_count=3)
    article_queryset = article_list[page_obj.start:page_obj.end]
    return render(request, 'home.html', locals())


# 个人站点
def site(request, username, **kwargs):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog
    article_list = models.Article.objects.filter(blog=blog).all()

    condition = kwargs.get('condition')
    param = kwargs.get('param')
    if kwargs:
        if condition == 'category':
            article_list = article_list.filter(category_id=param)
        elif condition == 'tag':
            article_list = article_list.filter(tags=param)
        else:
            year, month = param.split('-', 1)
            article_list = article_list.filter(create_time__year=year, create_time__month=month)

    page_obj = Pagination(request.GET.get('page', 1), article_list.count(), per_page_num=4, pager_count=3)
    article_queryset = article_list[page_obj.start:page_obj.end]

    return render(request, 'site.html', locals())


# 文章详情
def article_detail(request, username, article_id):
    comment_list = models.Comment.objects.filter(article_id=article_id).all()
    article_obj = models.Article.objects.filter(pk=article_id).first()
    return render(request, 'article_detail.html', locals())


import json

from django.db import transaction
from django.db.models import F


# 点赞点踩
def up_or_down(request):
    if request.is_ajax():
        back_dic = {"code": 100}
        if request.method == 'POST':
            if request.user.is_authenticated():
                user_id = request.user.pk
                article_id = request.POST.get('article_id')
                up_down = request.POST.get('up_down')
                up_down = json.loads(up_down)

                article_obj = models.Article.objects.filter(blog=request.user.blog, pk=article_id).first()
                if not article_obj:

                    is_up = models.UpAndDown.objects.filter(user_id=user_id, article_id=article_id).first()
                    if not is_up:

                        if up_down:
                            with transaction.atomic():
                                models.Article.objects.filter(pk=article_id).update(up_num=F('up_num') + 1)
                                models.UpAndDown.objects.create(article_id=article_id, user_id=user_id,
                                                                is_up=up_down)
                                back_dic['msg'] = '点赞成功'
                        else:
                            with transaction.atomic():
                                models.Article.objects.filter(pk=article_id).update(down_num=F('down_num') + 1)
                                models.UpAndDown.objects.create(article_id=article_id, user_id=user_id,
                                                                is_up=up_down)
                                back_dic['msg'] = '点踩成功'
                    else:
                        back_dic['code'] = 101
                        back_dic['msg'] = '您已经支持过了'
                else:
                    back_dic['code'] = 102
                    back_dic['msg'] = '凑不要脸的'

            else:
                back_dic['code'] = 103
                back_dic['msg'] = '请先<a data-toggle="modal" data-target="#myLogin">登录</a>'

        return JsonResponse(back_dic)


from django.contrib.auth.views import login_required


# 文章评论
@login_required
def article_comment(request):
    print(request.POST)
    if request.is_ajax():
        back_dic = {"code": 100}
        if request.method == 'POST':
            article_id = request.POST.get('article_id')
            content = request.POST.get('content')
            parent_id = request.POST.get('parent_id')
            user_id = request.user.pk
            if request.user.is_authenticated():
                if content:
                    with transaction.atomic():
                        models.Article.objects.filter(pk=article_id).update(comment_num=F('comment_num') + 1)
                        models.Comment.objects.create(
                            user_id=user_id, article_id=article_id,
                            content=content, parent_id=parent_id)
                        back_dic['msg'] = '评论成功'
                else:
                    back_dic['code'] = 101
                    back_dic['msg'] = '评论内容不能为空'
            else:
                back_dic['code'] = 102
                back_dic['msg'] = '请先<a data-toggle="modal" data-target="#myLogin">登录</a>'

        return JsonResponse(back_dic)


# 后台管理
@login_required
def backend(request):
    article_list = models.Article.objects.filter(blog=request.user.blog).all()
    page_obj = Pagination(request.GET.get('page', 1), article_list.count(), per_page_num=4, pager_count=3)
    article_queryset = article_list[page_obj.start:page_obj.end]
    return render(request, 'backend/backend.html', locals())


from bs4 import BeautifulSoup


# 添加文章
@login_required
def add_article(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        category_id = request.POST.get('category_id')
        tag_list = request.POST.getlist('tag_list')

        soup = BeautifulSoup(content)

        [tag.decompose() for tag in soup.find_all() if tag.name == 'script']

        desc = soup.text[0:150]

        article_obj = models.Article.objects.create(
            title=title,
            desc=desc,
            content=str(soup),
            category_id=category_id,
            blog=request.user.blog,
        )
        article_tag_list = [models.ArticleToTag(article=article_obj, tag_id=i) for i in tag_list]

        models.ArticleToTag.objects.bulk_create(article_tag_list)

        return redirect('backend_view')

    category_list = models.Category.objects.filter(blog=request.user.blog).all()
    tag_list = models.Tag.objects.filter(blog=request.user.blog).all()
    return render(request, 'backend/add_article.html', locals())


import os
from django.conf import settings


# 上传文件
def article_img(request):
    back_dic = {"error": 0}
    if request.method == 'POST':
        print(request.FILES)
        file_obj = request.FILES.get('imgFile')

        path = os.path.join(settings.BASE_DIR, 'media', 'article_img')

        if not os.path.exists(path):
            os.mkdir(path)

        file_path = os.path.join(path, file_obj.name)

        with open(file_path, 'wb') as f:
            [f.write(line) for line in file_obj.chunks()]

        back_dic['url'] = '/app01/media/article_img/%s' % file_obj.name

        return JsonResponse(back_dic)


# 修改头像
@login_required
def set_avatar(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('avatar')

        # models.UserInfo.objects.filter(blog=request.user.blog).update(avatar=file_obj)

        user_obj = models.UserInfo.objects.filter(blog=request.user.blog).first()
        user_obj.avatar = file_obj
        user_obj.save()
        return redirect('/app01/')
    return render(request, 'backend/set_avatar.html')
