from django import template
register = template.Library()


@register.simple_tag()
def loopcount(value, list):
    count = 0
    for a in list:
        if a == value:
            count += 1

    return count
