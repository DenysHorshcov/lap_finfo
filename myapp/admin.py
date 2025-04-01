from django.contrib import admin
from .models import Leagues, Countries, Players, Clubs, Matches, PlayersPositions

@admin.register(Leagues)
class LeaguesAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_title', 'country_id')
    search_fields = ('id','full_title', 'country__name')  # Allow searching by title & category name
    list_filter = ('full_title','country',)  # Add filter options in admin panel
    ordering = ('-id',)
    autocomplete_fields = ['country_id']

    def save_model(self, request, obj, form, change):
        if not obj.full_title:
            raise ValueError("full title name cannot be empty.")
        if not obj.country_id:
            raise ValueError("country id cannot be empty.")
        super().save_model(request, obj, form, change)

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

    def save_model(self, request, obj, form, change):
        if not obj.player_name:
            raise ValueError("Player name cannot be empty.")
        if not obj.birthday:
            raise ValueError("Birthday cannot be empty.")
        if not obj.current_club:
            raise ValueError("current club cannot be empty.")
        if not obj.country:
            raise ValueError("country cannot be empty.")
        super().save_model(request, obj, form, change)

@admin.register(PlayersPositions)
class PlayersPositionsAdmin(admin.ModelAdmin):
    list_display = ('players', 'positions')
    search_fields = ('players__player_name', 'positions__title')  # Allow searching by title & category name
    list_filter = ('players', 'positions')  # Add filter options in admin panel
    ordering = ('players',)

    def save_model(self, request, obj, form, change):
        if not obj.players or not obj.positions:
            raise ValueError("Both player and position are required.")
        super().save_model(request, obj, form, change)


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