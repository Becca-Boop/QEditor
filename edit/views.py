from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils.html import mark_safe




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
    room_list = QObject.objects.filter(category='room').order_by('name')
    item_list = QObject.objects.filter(category='item').order_by('name')
    context = {"room_list": room_list, "item_list": item_list}
    return render(request, "edit/object_list.html", context)
    
 
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

    
def object_page(request, object_id, page_id=-1):
    qobject = get_object_or_404(QObject, pk=object_id)
    if page_id == -1:
        page = MetaPage.get_home(qobject)
    else:
        page = MetaPage.objects.get(pk=page_id)
    print(page.name)
    mattrs = MetaAttr.objects.filter(page=page)
    qattrs = QAttr.objects.filter(qobject=qobject, attr__page=page)
    return render(request, "edit/object_detail.html", {"qobject": qobject, "mattrs":mattrs, "qattrs":qattrs, "page":page, "pages":MetaPage.get_some(qobject) })


def settings(request):
    settings = QObject.objects.get(name='settings')
    return redirect('/edit/object/' + str(settings.id))




def settings_js(request):
    return HttpResponse(QObject.get_settings_js(), content_type='text/javascript')

def data_js(request):
    return HttpResponse(QObject.get_js(), content_type='text/javascript')

def code_js(request):
    return HttpResponse("", content_type='text/javascript')

def style_css(request):
    return HttpResponse("", content_type='text/css')






def help(request, page):
    return render(request, "edit/help/" + page + ".html", {})


def error(request, error_str):
    return render(request, "edit/error.html", {"error":error_str})


