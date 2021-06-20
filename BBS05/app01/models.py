from django.db import models

# Create your models here.


from django.contrib.auth.models import AbstractUser


class UserInfo(AbstractUser):
    phone = models.CharField('手机号码', max_length=32, null=True, blank=True)

    create_time = models.DateField('注册时间', auto_now_add=True)

    avatar = models.FileField('头像', upload_to='avatar/', default='static/image/def.jpg')

    # 用户站点 一对一
    blog = models.OneToOneField(to='Site', null=True)

    class Meta:
        verbose_name_plural = '用户表'

    def __str__(self):
        return self.username


class Site(models.Model):
    site_name = models.CharField('站点名称', max_length=32)

    site_title = models.CharField('站点标题', max_length=32)

    site_theme = models.CharField('站点样式', max_length=32)

    class Meta:
        verbose_name_plural = '站点表'

    def __str__(self):
        return self.site_name


class Article(models.Model):
    title = models.CharField('文章标题', max_length=32)

    desc = models.CharField('文章简介', max_length=255)

    content = models.TextField('文章内容')

    create_time = models.DateField('发布时间', auto_now_add=True)

    # 数据库查询优化(普通字段)
    up_num = models.IntegerField('点赞数', default=0)

    down_num = models.IntegerField('点踩数', default=0)

    comment_num = models.IntegerField('评论数', default=0)

    article_read = models.IntegerField('阅读量', default=0)

    # 文章站点 一对多
    blog = models.ForeignKey(to='Site', null=True)

    # 文章分类 一对多
    category = models.ForeignKey(to='Category', null=True)

    # 文章标签 多对多 第三张表ArticleToTag
    tag = models.ManyToManyField(to='Tag', through='ArticleToTag', through_fields=('article', 'tag'))

    class Meta:
        verbose_name_plural = '文章表'

    def __str__(self):
        return self.title


class ArticleToTag(models.Model):
    article = models.ForeignKey(to='Article')
    tag = models.ForeignKey(to='Tag')

    class Meta:
        verbose_name_plural = '文章标签第三张表'


class Category(models.Model):
    name = models.CharField('文章分类', max_length=32)

    # 分类站点 一对多
    blog = models.ForeignKey(to='Site', null=True)

    class Meta:
        verbose_name_plural = '分类表'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('文章标签', max_length=32)

    # 分类标签 一对多
    blog = models.ForeignKey(to='Site', null=True)

    class Meta:
        verbose_name_plural = '标签表'

    def __str__(self):
        return self.name


class UpAndDown(models.Model):
    # 点赞点踩关联用户主键
    user = models.ForeignKey(to='UserInfo')

    # 点赞点踩关联文章主键
    article = models.ForeignKey(to='Article')
    is_up = models.BooleanField('点赞点踩')

    class Meta:
        verbose_name_plural = '点赞点踩表'


class Comment(models.Model):
    # 评论关联用户主键
    user = models.ForeignKey(to='UserInfo')

    # 被评论文章关联文章主键
    article = models.ForeignKey(to='Article')

    content = models.CharField('评论内容', max_length=255)

    comment_time = models.DateTimeField('评论时间', auto_now_add=True)

    # 子评论自关联
    parent = models.ForeignKey(to='self', null=True)

    class Meta:
        verbose_name_plural = '评论表'
