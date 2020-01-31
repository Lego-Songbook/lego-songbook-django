from django.contrib import admin

from .models import (
    Person,
    Plan,
    Position,
    PositionAssignment,
    Setlist,
    Song,
    SongArrangement,
    Team
)

# class SongbookAdminSite(admin.AdminSite):
#     site_header = "乐高曲库管理中心"
#
#
# admin_site = SongbookAdminSite(name="admin")


class PositionInline(admin.TabularInline):
    model = Position
    extra = 0
    filter_horizontal = ("people",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    # fields = ('name', 'positions')
    # filter_horizontal = ('positions',)
    inlines = [PositionInline]
    # filter_horizontal = ('positions',)
    search_fields = (
        "positions__people__first_name",
        "positions__people__last_name",
        # 'positions__people__nickname',
        "positions__name",
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ("age", "all_positions")
    list_display = ("full_name", "all_positions")
    # list_display_links = ('all_positions',)

    def all_positions(self, obj):
        return " | ".join([str(x) for x in obj.positions.all()])

    all_positions.short_description = "POSITIONS"


# @admin.register(Position)
# class PositionAdmin(admin.ModelAdmin):
#     fields = ('name', 'people', 'team')
#     filter_horizontal = ('people',)


class PlanArrangementThroughInline(admin.StackedInline):
    model = Plan.song_arrangements.through
    extra = 0


class PersonSchedulePlanThroughInline(admin.StackedInline):
    model = Plan.team_arrangement.through
    extra = 0


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    # fields = ('name', 'people', 'team')
    inlines = [PlanArrangementThroughInline, PersonSchedulePlanThroughInline]
    # filter_horizontal = ('arrangements', 'people')
    exclude = ("arrangements", "people")
    list_display = ("date", "worship_leader", "all_songs")

    def worship_leader(self, obj: Plan):
        return obj.team_arrangement.get(position__name="带领人").person

    def all_songs(self, obj: Plan):
        return ", ".join([str(x.song) for x in obj.song_arrangements.all()])

    all_songs.short_description = "SONGS"


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = ("name", "key", "sheet_type")
    readonly_fields = ("arrangements",)


admin.site.register(SongArrangement)
admin.site.register(Setlist)
admin.site.register(PositionAssignment)
