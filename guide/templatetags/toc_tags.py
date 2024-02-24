from django import template

register = template.Library()

@register.inclusion_tag('guide/toc.html')
def render_toc(toc_list):
    return {'toc_list': toc_list}

@register.filter
def multiply(value, arg):
    """乗算を行うカスタムテンプレートフィルター"""
    try:
        return value * arg
    except (ValueError, TypeError):
        return ''