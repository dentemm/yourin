from django import template

register = template.Library()

from django import template
register = template.Library()

@register.filter('form_class')
def form_class(obj):
    return obj.__class__.__name__

def has_menu_children(page):
    return page.get_children().live().in_menu().exists()

@register.assignment_tag(takes_context=True)
def get_site_root(context):
    # NB this returns a core.Page, not the implementation-specific model used
    # so object-comparison to self will return false as objects would differ
    return context['request'].site.root_page

# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the bootstrap menu requires
# a dropdown class to be applied to a parent
@register.inclusion_tag('home/partials/header.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().filter(
        live=True,
        show_in_menus=True
    )

    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)

    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

@register.simple_tag(takes_context=True)
def menuitems(context, parent, calling_page):
    '''
    Deze template tag retourneert de menu items
    Gebruik {% menuitems parent calling_page %}
    '''

    menuitems = parent.get_children().filter(
        live=True,
        show_in_menus=True
    )

    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)

    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }