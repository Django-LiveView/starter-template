from django import template

register = template.Library()


@register.filter
def concat(first_value, second_value):
    return first_value + str(second_value)

