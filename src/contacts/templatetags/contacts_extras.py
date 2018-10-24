from django import template

register = template.Library()


@register.filter
def queryset_to_list(value):
    return ", ".join([str(x) for x in value]) if value else "None"
