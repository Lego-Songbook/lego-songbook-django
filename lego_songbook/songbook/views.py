from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic

from .models import Song, Setlist

# Create your views here.

def index(request):
    return HttpResponse("Hello World.")


class SongView(generic.ListView):
    template_name = "songbook/song_list.html"
    context_object_name = "song_list"

    def get_queryset(self):
        """Return the list of all songs."""
        return Song.objects.order_by("name")


class SongDetailView(generic.DetailView):
    model = Song
    template_name = "songbook/song_detail.html"


class SetlistView(generic.ListView):
    template_name = "songbook/index.html"
    context_object_name = "setlist_list"


class SetlistDetailView(generic.DetailView):
    model = Setlist
    template_name = "songbook/setlist_detail.html"
