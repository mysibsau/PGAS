from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def create_link(value, arg):
    return reverse(f"achievements:create_{arg}", kwargs={"pk": value.pk})
