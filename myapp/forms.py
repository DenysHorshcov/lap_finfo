from django import forms
from .models import Leagues, Players, Clubs, Matches, PlayersPositions, Positions

class LeaguesForm(forms.ModelForm):
    class Meta:
        model = Leagues
        fields = ['id', 'full_title', 'country']

class PlayersForm(forms.ModelForm):

    current_club = forms.ModelChoiceField(
        queryset=Clubs.objects.all(),
        label="Current Club",
        empty_label="Select Club",
        widget=forms.Select(attrs={'class': 'form-control'})  # Optional: Bootstrap styling
    )

    class Meta:
        model = Players
        fields = ['player_name', 'birthday', 'current_club', 'country']

class ClubsForm(forms.ModelForm):
    class Meta:
        model = Clubs
        fields = ['full_title', 'location', 'stadium', 'league']

class MatchesForm(forms.ModelForm):
    class Meta:
        model = Matches
        fields = ['home_club', 'away_club', 'home_goals', 'away_goals', 'date']

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