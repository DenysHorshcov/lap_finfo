from django import forms
from .models import Leagues, Players, Clubs, Matches

class LeaguesForm(forms.ModelForm):
    class Meta:
        model = Leagues
        fields = ['id', 'full_title', 'country']

class PlayersForm(forms.ModelForm):
    class Meta:
        model = Players
        fields = ['id', 'player_name', 'birthday', 'current_club', 'country']

class ClubsForm(forms.ModelForm):
    class Meta:
        model = Clubs
        fields = ['id', 'full_title', 'location', 'stadium', 'league']

class MatchesForm(forms.ModelForm):
    class Meta:
        model = Matches
        fields = ['id', 'home_club', 'away_club', 'home_goals', 'away_goals', 'date']