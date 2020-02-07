from django.http import HttpResponse
from django.views import generic
from django_tables2 import SingleTableView

from .models import Song, Plan
from .tables import SongTable

# Create your views here.


def index(request):
    return HttpResponse("Hello World.")


class SongView(SingleTableView):
    model = Song
    table_class = SongTable
    template_name = "songbook/songs.html"
    context_object_name = "song_list"

    def get_queryset(self):
        """Return the list of all songs."""
        return Song.objects.order_by("name")


class SongDetailView(generic.DetailView):
    model = Song
    template_name = "songbook/song_detail.html"


class SetlistView(generic.ListView):
    template_name = "songbook/setlists.html"
    context_object_name = "setlist_list"

    def get_queryset(self):
        """Return the list of all songs."""
        return Plan.objects.order_by("date")


class SetlistDetailView(generic.DetailView):
    model = Plan
    template_name = "songbook/setlist_detail.html"
