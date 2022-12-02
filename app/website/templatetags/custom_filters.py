from django import template

register = template.Library()


@register.filter
def concat(first_value, second_value):
    return first_value + str(second_value)


@register.filter
def set_size(url, size):
    """
    {{ THUMBOR_URL|size: "1050x300" }}{% STATIC "img/algo.jpg"}
    return...
    https://thumbor.ccstech.dev/unsafe/1050x300/filters:format(webp)/https://ccstech.dev/static/img/algo.jpg
    """
    return url.replace("XsizeX", size)
