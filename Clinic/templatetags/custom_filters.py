from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def check_and_update_displayed(context, category_name):
    if 'displayed_categories' not in context:
        context['displayed_categories'] = []
    if category_name not in context['displayed_categories']:
        context['displayed_categories'].append(category_name)
        return True
    return False