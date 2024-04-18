from django.contrib import admin

from django.contrib import admin

from .models import *

admin.site.register(QGame)
admin.site.register(QObject)
admin.site.register(QAttr)
admin.site.register(MetaPage)
admin.site.register(MetaAttr)
admin.site.register(ItemToItemLinks)

