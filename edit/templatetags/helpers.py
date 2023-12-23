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






@register.filter
def to_html(s):
    if s.startswith('# '):
        return mark_safe('<h3>' + s[2:] + '</h3>')
    if s.startswith('## '):
        return mark_safe('<h4>' + s[2:] + '</h4>')

    return mark_safe('<p>' + s + '</p>')






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
    settings = qobject.qgame.get_settings()
    if not test_rules(qobject, settings, mattr):
        return ''
        
    value = qobject.get_attr(mattr.name)
    t = mattr.get_type()
    
    html = t.widget
    if isinstance(html, str):
        html = html.replace('*name*', mattr.name).replace('*value*', str(value))
    else:
        html = html(mattr, value, qobject)

    s = '<tr title="' + mattr.help_text + '">'
    s += '<td><b>' + mattr.display_name + '</b></td><td>'
    if not edit:
        s += value
        s += '</td><td>'
    elif t.big_widget:
        s += '</td><td>'
        s += mattr.help_text
        s += '</td></tr><tr><td colspan="3">' + html
    else:
        s += html
        s += '</td><td>'
        s += mattr.get_help_text()
    s += '</td></tr>'
    return mark_safe(s)
    
    
    
@register.simple_tag
def warnings():
    qgame = QGame.objects.first() # temp hack!!!!
    duplicates = qgame.get_duplicates()
    #print(duplicates)
    if duplicates:
        return mark_safe('<div class="warning">WARNING: Duplicated object names: ' + ', '.join(duplicates) + '</div>')
    else:
        return 'All good'




@register.simple_tag
def hier_shape(name, flag):
    return hier_triangle(name) if flag else hier_circle(name)


@register.simple_tag
def hier_triangle(name):
    s = ''
    s += '<svg width="12" height="12" id="svg-hide-for-' + name + '" class="svg-hide" style="display:none">'
    s += '  <polygon points="1,3 6,11 11,3" stroke="green" stroke-width="1" fill="yellow" onclick="hideList(\'' + name + '\')"/>'
    s += '</svg>'
    s += '<svg width="12" height="12" id="svg-show-for-' + name + '" class="svg-show">'
    s += '  <polygon points="3,1 10,6 3,11" stroke="green" stroke-width="1" fill="blue" onclick="showList(\'' + name + '\')"/>'
    s += '</svg>'
    return mark_safe(s)



@register.simple_tag
def hier_circle(name):
    s = ''
    s += '<svg width="12" height="12">'
    s += '<circle cx="6" cy="6" r="5" stroke="green" stroke-width="1" fill="grey" />'
    s += '</svg>'
    return mark_safe(s)

 



@register.simple_tag
def hier_obj(obj):
    flag = obj.has_contents()
    s = ''
    s += '<li>'
    s += hier_shape(obj.name, flag)

    s += '  <a href="/edit/object/' + str(obj.id) + '" target="_blank">'
    if obj.category == 'room':
        s += '<b>' + obj.display_name() + '</b>'
    else:
        s += obj.display_name()
    s += '</a>'
    if flag:
        s += '  <ul id="list-for-' + obj.name + '" style="display:none" class="show-hide">'
        for item in obj.get_contents():
            s += hier_obj(item)
        s += '</ul>'

    s += '</li>'
    return mark_safe(s)
