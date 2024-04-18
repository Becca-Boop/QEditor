from django.urls import path
from django.conf.urls import include

from . import views

app_name = "edit"

# Name is used by the reverse look up

urlpatterns = [

    path("object", views.object_list, name="object_list"),
    path("object/reset", views.reset, name="reset"),
    path("object/play", views.play, name="play"),
    path("object/<int:object_id>/", views.object_page, name="object_detail"),
    path("object/<int:object_id>/page/<str:page_id>", views.object_page, name="object_page"),
    path("object/<int:object_id>/edited", views.object_edited, name="object_edited"),
    
    path("object/region_added", views.region_added, name="region_added"),
    path("object/room_added", views.room_added, name="room_added"),
    path("object/<int:object_id>/item_added", views.item_added, name="item_added"),
    path("object/item_added", views.item_added_nowhere, name="item_added_nowhere"),
    path("object/<int:object_id>/exit_added", views.exit_added, name="exit_added"),
    path("object/<int:object_id>/link_added", views.link_added, name="link_added"),

    
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