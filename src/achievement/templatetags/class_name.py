from django import template

register = template.Library()


@register.filter
def class_name(value):
    return value._meta.model_name.lower()
