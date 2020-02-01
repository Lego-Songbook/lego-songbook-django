import pytest

from ...models import Song, SongArrangement

django_db = pytest.mark.django_db


@django_db
def test_song_arrangement_default_key():
    song = Song(name="Song", original_key="C")
    song.save()
    song_arr = SongArrangement(song=song)
    song_arr.save()

    assert song_arr.key == "C"
