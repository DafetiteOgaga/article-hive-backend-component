from django import template

register = template.Library()

@register.filter(name='atrs')
def atrs(field, attrs):
    attrs_dict = {}
    for attr in attrs.split(','):
        key, value = attr.split('=')
        attrs_dict[key] = value
    return field.as_widget(attrs=attrs_dict)
