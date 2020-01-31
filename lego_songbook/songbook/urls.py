from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = "songbook"
urlpatterns = [
    path("", TemplateView.as_view(template_name="songbook/index.html"), name="index"),
    path("songs/", views.SongView.as_view(), name="songs"),
    path("songs/<int:pk>/", views.SongDetailView.as_view(), name="song_detail"),
    path("setlists/", views.SetlistView.as_view(), name="setlists"),
    path("setlists/<int:pk>", views.SetlistDetailView.as_view(), name="setlist_detail"),
]
