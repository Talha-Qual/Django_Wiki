from django.urls import path

from . import views

app_name = "wiki"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/create_page", views.create_page, name="create_page"),
    path("wiki/random_page/", views.random_page, name="random_page"),
    path("wiki/edit_entry/<str:title>/", views.edit_entry, name="edit_entry"),
    path("wiki/<str:title>/", views.entry_page, name="title"),
]
