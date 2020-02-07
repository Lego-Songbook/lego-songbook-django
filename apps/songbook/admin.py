from django.contrib import admin
from songbook.models import (
    Person,
    Position,
    PositionAssignment,
    ServiceType,
    Song,
    Team,
    TeamArrangement,
)

from songbook.models import Plan  # Setlist,; SongArrangement,


class PositionInline(admin.TabularInline):
    model = Position
    extra = 0
    filter_horizontal = ("people",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [PositionInline]
    search_fields = (
        "positions__people__first_name",
        "positions__people__last_name",
        "positions__name",
    )


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    readonly_fields = ("age", "all_positions")
    list_display = ("full_name", "all_positions")

    def all_positions(self, obj):
        return " | ".join([str(x) for x in obj.positions.all()])

    all_positions.short_description = "POSITIONS"


# class PlanSongsThroughInline(admin.StackedInline):
#     model = Plan.songs.through
#     extra = 0
#
#
# class PlanTeamArrangementInline(admin.StackedInline):
#     model = TeamArrangement
#     extra = 0
#
#
# @admin.register(Plan)
# class PlanAdmin(admin.ModelAdmin):
#     inlines = [PlanSongsThroughInline, PlanTeamArrangementInline]
#     exclude = ("songs", "team_arrangement")
#     list_display = ("date", "worship_leader", "all_songs")
#
#     def worship_leader(self, obj: Plan):
#         return obj.team_arrangement.get(position__name="带领人").person
#
#     def all_songs(self, obj: Plan):
#         return ", ".join([str(x.song) for x in obj.songs.all()])
#
#     all_songs.short_description = "SONGS"


# @admin.register(Song)
# class SongAdmin(admin.ModelAdmin):
#     fields = (
#         "name",
#         "key",
#     )
#     # readonly_fields = ("songs",)


@admin.register(PositionAssignment)
class PositionAssignmentAdmin(admin.ModelAdmin):
    pass


class TeamArrangementPositionAssignmentThroughInline(admin.TabularInline):
    model = TeamArrangement.position_assignments.through
    extra = 0


@admin.register(TeamArrangement)
class TeamArrangementAdmin(admin.ModelAdmin):
    inlines = [TeamArrangementPositionAssignmentThroughInline]
    exclude = ("position_assignments",)


# admin.site.register(SongArrangement)
# admin.site.register(Setlist)
admin.site.register(ServiceType)
admin.site.register(Position)
admin.site.register(Song)
admin.site.register(Plan)


admin.site.site_header = "Lego Worship Administration"
admin.site.site_title = "Lego Worship Administration"
admin.site.index_title = "Site Admin"
admin.site.site_url = "/songbook"
