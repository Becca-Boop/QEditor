from django.urls import path
from django.conf.urls import include

from . import views

app_name = "edit"

# Name is used by the reverse look up

urlpatterns = [

    # Product
    # Cannot add or delete
    # Can edit the comment
    # Can create a batch for
    path("object", views.object_list, name="object_list"),
    path("object/reset", views.reset, name="reset"),
    path("object/play", views.play, name="play"),
    path("object/<int:object_id>/", views.object_page, name="object_detail"),
    path("object/<int:object_id>/page/<str:page_id>", views.object_page, name="object_page"),
    path("object/<int:object_id>/edited", views.object_edited, name="object_edited"),
    path("settings", views.settings, name="settings"),
    
    path("object/settings.js", views.settings_js, name="settings_js"),
    path("object/data.js", views.data_js, name="data_js"),
    path("object/code.js", views.code_js, name="code_js"),
    path("object/style.css", views.style_css, name="style_css"),
    


    # Misc
    path("", views.index, name="index"),
    path("reset", views.reset, name="reset"),
    path("help/<str:page>", views.help, name="help"),
    path("error/<str:error_str>", views.error, name="error"),
]