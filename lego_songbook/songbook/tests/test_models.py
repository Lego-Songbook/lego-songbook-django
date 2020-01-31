from django.test import TestCase

from ..models import Person, Position, Song, SongArrangement


class PersonModelTests(TestCase):
    def test_person_name_without_a_last_name(self):
        p = Person(first_name="John")
        p.save()
        self.assertEqual(str(p), "John")

    def test_person_name_chinese(self):
        p = Person(last_name="张", first_name="三")
        p.save()
        self.assertEqual(str(p), "张三")

    def test_person_name_english(self):
        p = Person(last_name="Bryant", first_name="Kobe")
        p.save()
        self.assertEqual(str(p), "Kobe Bryant")

    def test_default_nickname(self):
        p = Person(first_name="John")
        p.save()
        self.assertEqual(p.nickname, "John")

    def test_setting_nickname(self):
        p = Person(first_name="John", nickname="Johnny")
        p.save()
        self.assertEqual(p.nickname, "Johnny")


class PositionModelTest(TestCase):
    def test_get_all_people_in_a_position(self):
        p1 = Person(first_name="John")
        p2 = Person(first_name="Peter")
        p1.save()
        p2.save()
        pos = Position(name="Guitarist")
        pos.save()
        pos.people.set([p1, p2])
        all_guitarists = [str(x) for x in pos.people.all()]
        self.assertEqual(all_guitarists, ["John", "Peter"])

    def test_get_all_positions_of_a_person(self):
        p = Person(first_name="John")
        p.save()

        pos1 = Position(name="Guitarist")
        pos2 = Position(name="Keyboardist")
        pos1.save()
        pos2.save()
        pos1.people.set([p])
        pos2.people.set([p])

        all_positions = [str(x) for x in p.positions.all()]

        self.assertEqual(all_positions, ["Guitarist", "Keyboardist"])
        self.assertEqual(all_positions, p.all_positions)


class TestSongArrangement(TestCase):
    def test_song_arrangement_default_key(self):
        song = Song(name="Song", original_key="C")
        song.save()
        song_arr = SongArrangement(song=song)
        song_arr.save()
        self.assertEqual(song_arr.key, "C")
