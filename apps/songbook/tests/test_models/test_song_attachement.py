import shutil
import tempfile

from django.core.files import File
from django.test import TestCase
from django.utils import text

from ...models import Song, SongAttachment


class TestSongAttachment(TestCase):
    def test_attachment_path(self):
        """
        Attachments are uploaded to MEDIA_ROOT/songs/<media_type>/<song_name>.
        """
        song_sheet_file = File(tempfile.TemporaryFile())

        song = Song.objects.create(title="Song A")
        song_sheet = SongAttachment.objects.create(
            song=song, media_type="sheet", attachment=song_sheet_file
        )
        song_slug = text.slugify(song.title)
        assert song_sheet.attachment.name == (
            f"songbook/sheet/{song_slug}/{song_sheet_file.name}"
        )

    def tearDown(self) -> None:
        shutil.rmtree("./dev")
