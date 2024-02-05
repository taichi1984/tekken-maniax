from django import template

register = template.Library()

@register.inclusion_tag('guide/toc.html')
def render_toc(toc_list):
    return {'toc_list': toc_list}