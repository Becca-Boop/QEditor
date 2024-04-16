from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils.html import mark_safe

from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent
HELP_DIR = os.path.join(BASE_DIR, "help")



from .models import *


def index(request):
    return render(request, "edit/index.html", {})

def reset(request):
    kick_start()
    return redirect('/edit/object')

def play(request):
    code = '\n\n'
    for o in QObject.objects.all():
        code += o.to_js()
    context = {"code": mark_safe(code)}
    return render(request, "edit/play.html", context)

def object_list(request):
    qgame = QGame.objects.first()
    nowhere_list = qgame.get_not_attr(category='item', attr_name='loc')
    region_list = QObject.objects.filter(category='regn').order_by('name')
    #print(qgame)
    context = {"nowhere_list": nowhere_list, 'region_list':region_list, 'qgame':qgame}
    return render(request, "edit/region_list.html", context)
    #return render(request, "edit/object_list.html", context)
    
 
def object_edited(request, object_id):
    qobject = get_object_or_404(QObject, pk=object_id)
    old_page = MetaPage.get(qobject, request.POST['__old_page__'])
    qobject.update(request.POST, old_page)
    if '__template__' in request.POST and request.POST['__template__'] == 'yes':
        page = MetaPage.get(qobject, request.POST['__page__'])
        qobject.set_attr(page, True)
        qobject.save()
        return redirect('/edit/object/' + str(qobject.id) + '/page/' + str(page.id))
    
    elif request.POST['__page__'] == 'Close':
        return HttpResponse("<script>window.close()</script>")

    else:
        page = MetaPage.get(qobject, request.POST['__page__'])
        return redirect('/edit/object/' + str(qobject.id) + '/page/' + str(page.id))

    
def item_added(request, object_id):
    qobject = get_object_or_404(QObject, pk=object_id)
    name = request.POST['__name__']
    #print('item_added')
    #print(qobject.name)
    #print(name)

    new_object = QObject.objects.create(category='item', name=name, qgame=qobject.qgame)
    new_object.set_attr('loc', qobject.name)
    new_object.set_attr('gender', 'thirdperson')
    return redirect('/edit/object/' + str(new_object.id))

    
def item_added_nowhere(request):
    # actually adding an item, but putting it nowhere
    # TODO!!! needs a qgame!!!
    name = request.POST['__name__']

    new_object = QObject.objects.create(category='item', name=name)
    new_object.set_attr('gender', 'thirdperson')
    return redirect('/edit/object/' + str(new_object.id))


def link_added(request, object_id):
    qobject = get_object_or_404(QObject, pk=object_id)
    name = request.POST['__name__']
    item = request.POST['__giveitems__']
    success = request.POST['__success__']
    response = request.POST['__response__']


    new_object = ItemToItemLinks.objects.create(primaryitem=name, secondaryitem=item, success=success, response=response, link_type='give')
    return redirect('/edit/object/' + str(new_object.id))

    
def exit_added(request, object_id):
    print('=============================================')
    qobject = get_object_or_404(QObject, pk=object_id)
    print(qobject.name)
    name = request.POST['__name__']
    print(name)
    direction = request.POST['__dir__']
    print(direction)
    dest = QObject.objects.get(name=name)

    new_object = qobject.create_exit(dest, direction)
    print('About to redirect')
    return redirect('/edit/object/' + str(new_object.id))

    
def room_added(request):
    name = request.POST['__name__']
    region_name = request.POST['__region__']
    region = QObject.objects.get(name=region_name)

    new_object = QObject.objects.create(category='room', name=name, qgame=region.qgame)
    new_object.set_attr('region', region.name)
    return redirect('/edit/object/' + str(new_object.id))

def region_added(request):
    # !!! TODO
    name = request.POST['__name__']

    new_object = QObject.objects.create(category='regn', name=name)
    return redirect('/edit/object/' + str(new_object.id))

    
def object_page(request, object_id, page_id=-1):
    qobject = get_object_or_404(QObject, pk=object_id)
    if page_id == -1:
        page = MetaPage.get_home(qobject)
    else:
        page = MetaPage.objects.get(pk=page_id)
    mattrs = MetaAttr.objects.filter(page=page)
    qattrs = QAttr.objects.filter(qobject=qobject, attr__page=page)
    return render(request, "edit/object_detail.html", {"qobject": qobject, "mattrs":mattrs, "qattrs":qattrs, "page":page, "pages":MetaPage.get_some(qobject), 'title':'QJS: ' + qobject.name })


def settings(request):
    settings = QObject.objects.get(name='settings')
    return redirect('/edit/object/' + str(settings.id))




def settings_js(request):
    qgame = QGame.objects.first()
    return HttpResponse(qgame.to_settings_js(), content_type='text/javascript')

def data_js(request):
    qgame = QGame.objects.first()
    return HttpResponse(qgame.to_data_js(), content_type='text/javascript')

def code_js(request):
    return HttpResponse("", content_type='text/javascript')

def style_css(request):
    return HttpResponse("", content_type='text/css')






def help(request, page):
    path = os.path.join(BASE_DIR, "edit", "help", page + ".txt")
    print(path)
    lines = ['File not found']
    f = open(path, "r")
    try:
        lines = f.readlines()
    finally:
        f.close()

    return render(request, "edit/help.html", {"data":lines})
    #return render(request, "edit/help/" + page + ".html", {})


def error(request, error_str):
    return render(request, "edit/error.html", {"error":error_str})


