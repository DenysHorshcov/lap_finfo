from django import forms
from .models import Leagues, Players, Clubs, Matches, PlayersPositions, Positions

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

class PlayersPositionsForm(forms.ModelForm):
    class Meta:
        model = PlayersPositions
        fields = ['players', 'positions']

    def clean(self):
        cleaned_data = super().clean()
        player = cleaned_data.get("players")
        position = cleaned_data.get("positions")

        # ✅ Check if this player-position combination already exists
        if PlayersPositions.objects.filter(players=player, positions=position).exists():
            raise forms.ValidationError("This player is already assigned to this position.")

        return cleaned_data