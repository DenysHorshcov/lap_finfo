from django.urls import path
from .views import main_page, add_league, edit_league, delete_league_confirm, players_page, add_player, edit_player, delete_player_confirm, clubs_page, add_club, edit_club, delete_club_confirm, matches_page, add_match, edit_match, delete_match_confirm, leagues_page, league_detail, club_detail, player_detail, player_position_page, add_player_position, edit_player_position, delete_player_position

urlpatterns = [
    path('', main_page, name='main_page'),
    path('l/', leagues_page, name='leagues_page'),
    path('add_l/', add_league, name='add_league'),
    path('edit_l/<int:league_id>/', edit_league, name='edit_league'),
    path('delete_l/<int:league_id>/', delete_league_confirm, name='delete_league_confirm'),
    path('p/', players_page, name='players_page'),
    path('add_p/', add_player, name='add_player'),
    path('edit_p/<int:player_id>/', edit_player, name='edit_player'),
    path('delete_p/<int:player_id>/', delete_player_confirm, name='delete_player_confirm'),
    path('c/', clubs_page, name='clubs_page'),
    path('add_c/', add_club, name='add_club'),
    path('edit_c/<int:club_id>/', edit_club, name='edit_club'),
    path('delete_c/<int:club_id>/', delete_club_confirm, name='delete_club_confirm'),
    path('m/', matches_page, name='matches_page'),
    path('add_m/', add_match, name='add_match'),
    path('edit_m/<int:match_id>/', edit_match, name='edit_match'),
    path('delete_m/<int:match_id>/', delete_match_confirm, name='delete_match_confirm'),
    path('pp/', player_position_page, name='players_positions'),
    path('add_pp/', add_player_position, name='add_player_position'),
    path('edit_pp/<int:player_id>/<int:position_id>/', edit_player_position, name='edit_player_position'),
    path('delete_pp/<int:player_id>/<int:position_id>/', delete_player_position, name='delete_player_position'),

    path('league/<int:league_id>/', league_detail, name='league_detail'),
    path('club/<int:club_id>/', club_detail, name='club_detail'),
    path('player/<int:player_id>/', player_detail, name='player_detail'),
]