import django_tables2 as tables
# from django.db.models import F
# from pypinyin import lazy_pinyin

from .models import Song


class SongTable(tables.Table):
    sheet_type = tables.Column(orderable=False)

    class Meta:
        model = Song
        # template_name = "django_tables2/bootstrap.html"
        fields = ("name", "key", "sheet_type")
        attrs = {"td": {"style": "text-align: center"}}

    # def order_name(self, queryset, is_descending):
    #     """Order the name column by its pinyin."""
    #     queryset = queryset.annotate(
    #         pinyin=[pinyin.lower() for pinyin in lazy_pinyin(F('name').split(" "))]
    #     ).order_by(f"{'-' if is_descending else ''}pinyin")
    #     return queryset, True
    #
    # def order_key(self, queryset, is_descending):
    #     """Order the key column properly."""
    #     queryset = queryset.annotate(
    #         key_value=F("key")
    #     ).order_by(f"{'-' if is_descending else ''}key_value")
    #     return queryset, True
