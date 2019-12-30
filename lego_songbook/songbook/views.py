from django.shortcuts import render
from django.views import generic
from .models import Song, Setlist
# Create your views here.


class SongView(generic.ListView):
    model = Song
    template_name = "songbook/songs.html"
    # context_object_name = "song_list"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["song_list"] = self.model.
