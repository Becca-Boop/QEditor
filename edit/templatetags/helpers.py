from django import template
from django.utils.html import mark_safe
import datetime
from edit.quest_data import *
from edit.models import *

register = template.Library()


@register.filter
def truncate(str, n):
    if len(str) < n:
        return str
    return str[:n] + '...'



@register.simple_tag
def page_button(opt, page):
    s = '<input type="button" value="' + opt.alias + '" onclick="submit_page(\'' + opt.name + '\')"'
    if opt == page:
        s += ' disabled'
    s += '/>'
    return mark_safe(s)
   
    




@register.simple_tag
def help_link(page, name = None):
    if not page:
        return ''
        
    if not name:
        name = page.title()
    # should be a better way to do this using the url helper but I cannot find where that is to import it!
    return mark_safe('<p>Help: <a href="/edit/help/' + page + '" target="_blank">' + name + '</a></p>')




@register.simple_tag
def attr_row(mattr, qobject, edit=True):
    # check if applicable
    if not test_rules(qobject, mattr):
        return ''
        
    value = qobject.get_attr(mattr.name)
    widget = mattr.get_type()
    
    html = widget[3]
    if isinstance(html, str):
        html = html.replace('*name*', mattr.name).replace('*value*', str(value))
    else:
        html = html(mattr, value)

    s = '<tr title="' + mattr.help_text + '">'
    s += '<td><b>' + mattr.display_name + '</b></td><td>'
    if not edit:
        s += value
        s += '</td><td>'
    elif widget[2]:
        s += '</td><td>'
        s += mattr.help_text
        s += '</td></tr><tr><td colspan="3">' + html
    else:
        s += html
        s += '</td><td>'
        s += mattr.get_help_text()
    s += '</td></tr>'
    return mark_safe(s)
    
    
    
