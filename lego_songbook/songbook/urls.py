from django.urls import path

from . import views


app_name = "songbook"
urlpatterns = [
    path('', views.index, name='index'),
    path("songs/", views.SongView.as_view(), name="songs"),
    path("song/<int:pk>/", views.SongDetailView.as_view(), name="song_detail"),
    path("setlists/", views.SetlistView.as_view(), name="setlists"),
    path("setlist/<int:pk>", views.SetlistDetailView.as_view(),         name="setlist_detail"),
]
