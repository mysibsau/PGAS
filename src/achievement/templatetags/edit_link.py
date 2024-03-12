from django import template
from django.urls import reverse

register = template.Library()


@register.filter
def edit_link(value):
    model_name = value._meta.model_name
    return reverse(f'achievements:{model_name}_edit', kwargs={'pk': value.pk})
