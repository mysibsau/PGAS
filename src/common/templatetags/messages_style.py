from django import template
from django.contrib import messages

register = template.Library()


@register.filter(is_safe=True)
def messages_style(value):
    styles = {
        messages.DEBUG: "alert alert-secondary",
        messages.INFO: "alert alert-primary",
        messages.SUCCESS: "alert alert-success",
        messages.WARNING: "alert alert-warning",
        messages.ERROR: "alert alert-danger",
    }
    return styles[value]
