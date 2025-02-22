from django.shortcuts import render, redirect, get_object_or_404
from .models import Leagues, Players, Clubs, Matches
from .forms import LeaguesForm, PlayersForm, ClubsForm, MatchesForm

# Create your views here.
def main_page(request):
    return render(request, 'myapp/main_page.html', {})

def leagues_page(request):
    data = Leagues.objects.all()
    return render(request, 'myapp/leagues_page.html', {'data': data})

def players_page(request):
    data = Players.objects.all()
    return render(request, 'myapp/players_page.html', {'data': data})

def clubs_page(request):
    data = Clubs.objects.all()
    return render(request, 'myapp/clubs_page.html', {'data': data})

def matches_page(request):
    data = Matches.objects.all()
    return render(request, 'myapp/matches_page.html', {'data': data})

def add_match(request):
    if request.method == "POST":
        form = MatchesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('matches_page')  # Redirect to main page
    else:
        form = MatchesForm()
    
    return render(request, 'myapp/forms/add_match.html', {'form': form})

def edit_match(request, match_id):
    match = get_object_or_404(Matches, id=match_id)
    if request.method == "POST":
        form = MatchesForm(request.POST, instance=match)
        if form.is_valid():
            form.save()
            return redirect('matches_page')
    else:
        form = MatchesForm(instance=match)
    
    return render(request, 'myapp/forms/edit_match.html', {'form': form})

def delete_match_confirm(request, match_id):
    match = get_object_or_404(Matches, id=match_id)
    if request.method == "POST":  # If user confirms deletion
        match.delete()
        return redirect('matches_page')

    return render(request, 'myapp/forms/delete_match_confirm.html', {'match': match})

def add_league(request):
    if request.method == "POST":
        form = LeaguesForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('main_page')  # Redirect to main page
    else:
        form = LeaguesForm()
    
    return render(request, 'myapp/forms/add_league.html', {'form': form})

def edit_league(request, league_id):
    league = get_object_or_404(Leagues, id=league_id)
    if request.method == "POST":
        form = LeaguesForm(request.POST, instance=league)
        if form.is_valid():
            form.save()
            return redirect('main_page')
    else:
        form = LeaguesForm(instance=league)
    
    return render(request, 'myapp/forms/edit_league.html', {'form': form})

def delete_league_confirm(request, league_id):
    league = get_object_or_404(Leagues, id=league_id)
    if request.method == "POST":  # If user confirms deletion
        league.delete()
        return redirect('main_page')

    return render(request, 'myapp/forms/delete_league_confirm.html', {'league': league})

def add_player(request):
    if request.method == "POST":
        form = PlayersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('players_page')  # Redirect to main page
    else:
        form = PlayersForm()
    
    return render(request, 'myapp/forms/add_player.html', {'form': form})

def edit_player(request, player_id):
    player = get_object_or_404(Players, id=player_id)
    if request.method == "POST":
        form = PlayersForm(request.POST, instance=player)
        if form.is_valid():
            form.save()
            return redirect('players_page')
    else:
        form = PlayersForm(instance=player)
    
    return render(request, 'myapp/forms/edit_player.html', {'form': form})

def delete_player_confirm(request, player_id):
    player = get_object_or_404(Players, id=player_id)
    if request.method == "POST":  # If user confirms deletion
        player.delete()
        return redirect('players_page')

    return render(request, 'myapp/forms/delete_player_confirm.html', {'player': player})


def add_club(request):
    if request.method == "POST":
        form = ClubsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('clubs_page')  # Redirect to main page
    else:
        form = ClubsForm()
    
    return render(request, 'myapp/forms/add_club.html', {'form': form})

def edit_club(request, club_id):
    club = get_object_or_404(Clubs, id=club_id)
    if request.method == "POST":
        form = ClubsForm(request.POST, instance=club)
        if form.is_valid():
            form.save()
            return redirect('clubs_page')
    else:
        form = ClubsForm(instance=club)
    
    return render(request, 'myapp/forms/edit_club.html', {'form': form})

def delete_club_confirm(request, club_id):
    club = get_object_or_404(Clubs, id=club_id)
    if request.method == "POST":  # If user confirms deletion
        club.delete()
        return redirect('clubs_page')

    return render(request, 'myapp/forms/delete_club_confirm.html', {'club': club})

def league_detail(request, league_id):
    league = get_object_or_404(Leagues, id=league_id)
    clubs = Clubs.objects.filter(league = league.id)
    club_ids = clubs.values_list('id', flat=True)

    # Get matches where home_club_id or away_club_id is in club_ids
    matches = Matches.objects.filter(home_club__in=club_ids) | Matches.objects.filter(away_club__in=club_ids)

    standings = {club.id: {"club": club, "points": 0, "wins": 0, "draws": 0, "losses": 0} for club in clubs}

    # Process each match
    for match in matches:
        if match.home_goals is None or match.away_goals is None:
            continue  # Skip matches without a result

        # Get home and away clubs
        home_club = match.home_club
        away_club = match.away_club

        # Determine result
        if match.home_goals > match.away_goals:
            standings[home_club.id]["wins"] += 1
            standings[home_club.id]["points"] += 3
            standings[away_club.id]["losses"] += 1
        elif match.home_goals < match.away_goals:
            standings[away_club.id]["wins"] += 1
            standings[away_club.id]["points"] += 3
            standings[home_club.id]["losses"] += 1
        else:  # Draw
            standings[home_club.id]["draws"] += 1
            standings[away_club.id]["draws"] += 1
            standings[home_club.id]["points"] += 1
            standings[away_club.id]["points"] += 1

    # Convert standings dict to sorted list (by points, then wins)
    standings_list = sorted(
        standings.values(), key=lambda x: (-x["points"], -x["wins"], -x["draws"], x["losses"])
    )

    return render(request, 'myapp/details/league_detail.html', {'league': league, 'standings': standings_list, 'matches': matches})