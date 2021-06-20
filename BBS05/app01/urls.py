from django.conf.urls import url
from app01 import views
from django.views.static import serve
from django.conf import settings

urlpatterns = [
    # home主页
    url(r'^$', views.home, name='home_view'),
    # 注册接口
    url(r'^register/', views.register, name='register_view'),
    # 登录接口
    url(r'^login/', views.login, name='login_view'),
    # 退出登录
    url(r'^logout/', views.logout, name='logout_view'),
    # 暴露用户文件media
    url(r'^media/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),
    # 随机验证码
    url(r'^random_num/', views.random_num, name='random_num_view'),
    # 修改密码
    url(r'^set_password/', views.set_password, name='set_password_view'),
    # 点赞点踩
    url(r'^UpAndDown/', views.UpAndDown, name='UpAndDown_view'),
    # 文章评论
    url(r'^article_comment/', views.article_comment, name='article_comment_view'),

    # 后台管理
    url(r'^backend/', views.backend, name='backend_view'),
    # 添加文章
    url(r'^add_article/', views.add_article, name='add_article_view'),
    # 上传用户文件
    url(r'article_file/',views.article_file,name='article_file_view'),
    # 修改头像
    url(r'^set_avatar/',views.set_avatar,name='set_avatar_view'),

    # 个人站点
    url(r'^(?P<username>\w+)/$', views.site, name='site_view'),
    # 左侧菜单栏筛选
    url(r'^(?P<username>\w+)/(?P<condition>(category|tag|archive))/(?P<param>.*)/', views.site),
    # 文章详情页
    url(r'^(?P<username>\w+)/article/(?P<article_id>\d+)/', views.article_detail, name='article_detail_view'),

]
