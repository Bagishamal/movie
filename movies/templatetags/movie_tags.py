from django import template
from ..models import *

register = template.Library()

@register.simple_tag(name='category_name')
def smth():
    return Category.objects.all()


@register.simple_tag()
def last_changes(number = 1):
    last_five = Movie.objects.reverse()[:number]
    return last_five

# @register.inclusion_tag("movies/base.html")
# def get_last_posts(number=1):
#     last = Movie.objects.reverse()[:number]
#     return last