from django import template
from lit.models import Category

register = template.Library()

@register.inclusion_tag('lit/cats.html')
def get_category_list():
    return {'cats': Category.objects.all()}
