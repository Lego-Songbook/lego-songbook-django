from django.contrib import admin

from songbook.models import (
    Person,
    Plan,
    Position,
    PositionAssignment,
    ServiceType,
    Setlist,
    Song,
    SongArrangement,
    Team,
    TeamArrangement,
)


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


class PlanArrangementThroughInline(admin.StackedInline):
    model = Plan.song_arrangements.through
    extra = 0


class PersonSchedulePlanThroughInline(admin.StackedInline):
    model = Plan.team_arrangement.through
    extra = 0


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    inlines = [PlanArrangementThroughInline, PersonSchedulePlanThroughInline]
    exclude = ("song_arrangements", "team_arrangement")
    list_display = ("date", "worship_leader", "all_songs")

    def worship_leader(self, obj: Plan):
        return obj.team_arrangement.get(position__name="带领人").person

    def all_songs(self, obj: Plan):
        return ", ".join([str(x.song) for x in obj.song_arrangements.all()])

    all_songs.short_description = "SONGS"


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    fields = (
        "name",
        "original_key",
    )
    readonly_fields = ("song_arrangements",)


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


admin.site.register(SongArrangement)
admin.site.register(Setlist)
admin.site.register(ServiceType)
admin.site.register(Position)
admin.site.site_header = "Lego Worship Administration"
admin.site.site_title = "Lego Worship Administration"
admin.site.index_title = "Site Admin"
admin.site.site_url = "/songbook"
