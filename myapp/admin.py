from django.contrib import admin
from .models import Leagues, Countries, Players, Clubs, Matches, PlayersPositions

@admin.register(Leagues)
class LeaguesAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title', 'country_id')
    search_fields = ('id','full_title', 'country__name')  # Allow searching by title & category name
    list_filter = ('full_title','country',)  # Add filter options in admin panel
    ordering = ('-id',)
    autocomplete_fields = ['country_id']

@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
    list_display = ('id', 'player_name', 'birthday', 'current_club', 'country')
    search_fields = ('id', 'player_name', 'birthday', 'current_club', 'country')  # Allow searching by title & category name
    list_filter = ('player_name', 'birthday', 'current_club','country',)  # Add filter options in admin panel
    ordering = ('-id',)
    autocomplete_fields = ['country_id', 'current_club_id']
    def current_club_display(self, obj):
        return obj.current_club.full_title  # ✅ Show club title in admin panel
    current_club_display.admin_order_field = 'current_club'  # Allow sorting
    current_club_display.short_description = 'Club'  # Change column name

@admin.register(PlayersPositions)
class PlayersPositionsAdmin(admin.ModelAdmin):
    list_display = ('players', 'positions')
    search_fields = ('players__player_name', 'positions__title')  # Allow searching by title & category name
    list_filter = ('players', 'positions')  # Add filter options in admin panel
    ordering = ('players',)


@admin.register(Clubs)
class ClubsAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title', 'location', 'stadium', 'league')
    search_fields = ('id', 'full_title', 'location', 'stadium', 'league')  # Allow searching by title & category name
    list_filter = ('full_title', 'location', 'stadium', 'league')  # Add filter options in admin panel
    ordering = ('-id',)
    autocomplete_fields = ['league_id']

@admin.register(Matches)
class MatchesAdmin(admin.ModelAdmin):
    list_display = ('id', 'home_club', 'away_club', 'home_goals', 'away_goals', 'date')
    search_fields = ('id', 'home_club', 'away_club', 'home_goals', 'away_goals', 'date')  # Allow searching by title & category name
    list_filter = ('home_club', 'away_club', 'home_goals', 'away_goals', 'date')  # Add filter options in admin panel
    ordering = ('-id',)
    autocomplete_fields = ['home_club_id', 'away_club_id']

@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title')
    search_fields = ('full_title',)


# ✅ Check if Players is already registered before adding it
if not admin.site.is_registered(Players):
    admin.site.register(Players, PlayersAdmin)