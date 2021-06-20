from django.template import Library

register = Library()
from app01 import models
from django.db.models import F, Count
from django.db.models.functions import TruncMonth


@register.inclusion_tag('left_menu.html')
def left(username):
    user_obj = models.UserInfo.objects.filter(username=username).first()
    blog = user_obj.blog

    category_list = models.Category.objects.filter(blog=blog) \
        .annotate(num=Count('article__id')).values('name', 'num', 'pk')

    tag_list = models.Tag.objects.filter(blog=blog) \
        .annotate(num=Count('article__id')).values('name', 'num', 'pk')

    date_list = models.Article.objects.filter(blog=blog) \
        .annotate(month=TruncMonth('create_time')).values('month').annotate(num=Count('pk')).values('month', 'num')

    return locals()
