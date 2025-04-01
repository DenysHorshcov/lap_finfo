from django import forms
from .models import Leagues, Players, Clubs, Matches, PlayersPositions, Positions
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date
from dateutil.relativedelta import relativedelta

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username","email", "password1", "password2"]
        
class LeaguesForm(forms.ModelForm):
    class Meta:
        model = Leagues
        fields = ['id', 'full_title', 'country']
    
    def clean_full_title(self):
        full_title = self.cleaned_data.get('full_title')
        if not full_title:
            raise forms.ValidationError("League title cannot be empty.")
        return full_title
    
    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise forms.ValidationError("country title cannot be empty.")
        return country

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
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
        }
    
    def clean_player_name(self):
        player_name = self.cleaned_data.get('player_name')
        if not player_name:
            raise forms.ValidationError("Player name cannot be empty.")
        return player_name

    def clean_birthday(self):
        birthday = self.cleaned_data.get('birthday')
        if birthday and (birthday > (date.today() - relativedelta(years=14)) or birthday < date(1975, 1, 1)):
            
            raise forms.ValidationError("The date cannot be in the future.")
        if not birthday:
            raise forms.ValidationError("Birthday cannot be empty.")
        return birthday
    
    def clean_current_club(self):
        current_club = self.cleaned_data.get('current_club')
        if not current_club:
            raise forms.ValidationError("Club must be selected.")
        return current_club
    
    def clean_country(self):
        country = self.cleaned_data.get('country')
        if not country:
            raise forms.ValidationError("Country cannot be empty.")
        return country
    


class ClubsForm(forms.ModelForm):
    class Meta:
        model = Clubs
        fields = ['full_title', 'location', 'stadium', 'league']
    
    def clean_full_title(self):
        full_title = self.cleaned_data.get('full_title')
        if not full_title:
            raise forms.ValidationError("Club title cannot be empty.")
        return full_title
    
    def clean_location(self):
        location = self.cleaned_data.get('location')
        if not location:
            raise forms.ValidationError("location title cannot be empty.")
        return location
    
    def clean_stadium(self):
        stadium = self.cleaned_data.get('stadium')
        if not stadium:
            raise forms.ValidationError("stadium title cannot be empty.")
        return stadium
    
    def clean_league(self):
        league = self.cleaned_data.get('league')
        if not league:
            raise forms.ValidationError("league title cannot be empty.")
        return league


class MatchesForm(forms.ModelForm):
    class Meta:
        model = Matches
        fields = ['home_club', 'away_club', 'home_goals', 'away_goals', 'date']
    
    def clean(self):
        cleaned_data = super().clean()
        home_club = cleaned_data.get("home_club")
        away_club = cleaned_data.get("away_club")

        if home_club == away_club:
            raise forms.ValidationError("Home and away clubs cannot be the same.")
        
        if not cleaned_data.get("date"):
            raise forms.ValidationError("Match date cannot be empty.")
        
        if not cleaned_data.get("home_goals"):
            raise forms.ValidationError("Match date cannot be empty.")
        
        if not cleaned_data.get("away_goals"):
            raise forms.ValidationError("Match date cannot be empty.")

        return cleaned_data

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