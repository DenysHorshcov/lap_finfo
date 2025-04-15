from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from .models import Leagues, Players, Clubs, Matches, PlayersPositions, Positions, FavoriteMatch
from django.db import connection
from django.contrib import messages
from .forms import LeaguesForm, PlayersForm, ClubsForm, MatchesForm, PlayersPositionsForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm
from django.contrib.auth.forms import AuthenticationForm
from django.db import IntegrityError
from django.db import models

from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .models_ext import Profile, UnbanRequest

def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.email = form.cleaned_data.get('email')
            user.save()
            return redirect('main_page')
    else:
        form = RegisterForm()
    return render(request, 'myapp/register.html', {'form': form})

def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main_page')
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {'form': form})

def logout_user(request):
    logout(request)
    return redirect('main_page')

# Create your views here.
def main_page(request):
    if hasattr(request.user, 'profile') and request.user.profile.is_banned:
        if request.method == 'POST':
            message = request.POST.get('message', '').strip()
            if message:
                UnbanRequest.objects.update_or_create(user=request.user, defaults={'message': message})
                messages.success(request, "Your unban request has been submitted.")
    return render(request, 'myapp/main_page.html')

def leagues_page(request):
    data = Leagues.objects.all()
    return render(request, 'myapp/leagues_page.html', {'data': data})

def players_page(request):
    name_query = request.GET.get('player_name')
    club_query = request.GET.get('club_name')

    data = Players.objects.all()

    if name_query:
        data = data.filter(player_name__icontains=name_query)

    if club_query:
        data = data.filter(current_club__full_title__icontains=club_query)

    return render(request, 'myapp/players_page.html', {
        'data': data,
        'player_name': name_query,
        'club_name': club_query
    })

def clubs_page(request):
    club_query = request.GET.get('club_title')
    league_query = request.GET.get('league_title')

    data = Clubs.objects.all()

    if club_query:
        data = data.filter(full_title__icontains=club_query)

    if league_query:
        data = data.filter(league__full_title__icontains=league_query)

    return render(request, 'myapp/clubs_page.html', {
        'data': data,
        'club_title': club_query,
        'league_title': league_query
    })

def matches_page(request):
    data = Matches.objects.all()
    query = request.GET.get('q')
    favorites = []

    if request.user.is_authenticated and not request.user.is_superuser:
        favorites = FavoriteMatch.objects.filter(user=request.user).values_list('match_id', flat=True)
    
    if query:
        data = Matches.objects.filter(
            models.Q(home_club__full_title__icontains=query) |
            models.Q(away_club__full_title__icontains=query)
        )
    else:
        data = Matches.objects.all()

    return render(request, 'myapp/matches_page.html', {
        'data': data,
        'query': query,
        'favorites': favorites
    })

def player_position_page(request):
    players_positions = PlayersPositions.objects.select_related('players', 'positions').values(
    'players__id', 'players__player_name',  # ✅ Correct field from Players table
    'positions__id', 'positions__title'  # ✅ Correct field from Positions table
    )

    player = request.GET.get('player')
    position = request.GET.get('position')

    if player:
        players_positions = players_positions.filter(players__player_name__icontains=player)

    if position:
        players_positions = players_positions.filter(positions__title__icontains=position)

    return render(request, 'myapp/players_positions.html', {'players_positions': players_positions, 'player': player,
        'position': position
    })

def add_player_position(request):
    if request.method == "POST":
        form = PlayersPositionsForm(request.POST)
        if form.is_valid():
            # ✅ Ensure the entry is unique before saving
            player = form.cleaned_data['players']
            position = form.cleaned_data['positions']
            
            if not PlayersPositions.objects.filter(players=player, positions=position).exists():
                with connection.cursor() as cursor:
                    cursor.execute(
                        'INSERT INTO "Players_Positions" ("Players_id", "Positions_id") VALUES (%s, %s)',
                        [player.id, position.id]
                    )
                messages.success(request, "Player position added successfully.")
                return redirect('players_positions')
            else:
                messages.error(request, "This player is already assigned to this position.")
    else:
        form = PlayersPositionsForm()
    
    return render(request, 'myapp/forms/add_player_position.html', {'form': form})

def edit_player_position(request, player_id, position_id):
    if request.method == "POST":
        form = PlayersPositionsForm(request.POST)
        if form.is_valid():
            # ✅ Manually update the foreign key values instead of using .save()
            with connection.cursor() as cursor:
                cursor.execute(
                    'UPDATE "Players_Positions" SET "Players_id" = %s, "Positions_id" = %s WHERE "Players_id" = %s AND "Positions_id" = %s',
                    [form.cleaned_data['players'].id, form.cleaned_data['positions'].id, player_id, position_id]
                )
            return redirect('players_positions')

    else:
        form = PlayersPositionsForm(initial={'players': player_id, 'positions': position_id})

    return render(request, 'myapp/forms/edit_player_position.html', {'form': form})

def delete_player_position(request, player_id, position_id):
    if request.method == "POST":
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    'DELETE FROM "Players_Positions" WHERE "Players_id" = %s AND "Positions_id" = %s',
                    [player_id, position_id]
                )
        except IntegrityError:
            messages.error(request, "Cannot delete this position because it is referenced in another table.")
        return redirect('players_positions')

    return render(request, 'myapp/forms/delete_player_position.html', {'player_id': player_id, 'position_id': position_id})


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
        try:
            match.delete()
            messages.success(request, "Match deleted successfully.")
        except IntegrityError:
            messages.error(request, "Cannot delete this match because it is referenced in another table.")
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
        try:
            league.delete()
            messages.success(request, "League deleted successfully.")
        except IntegrityError:
            messages.error(request, "Cannot delete this league because it is referenced in another table.")
        return redirect('leagues_page')

    return render(request, 'myapp/forms/delete_league_confirm.html', {'league': league})

def add_player(request):
    if request.method == "POST":
        form = PlayersForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Player added successfully!")
            return redirect('players_page')  # Redirect to main page
        else:
            messages.error(request, "Please correct the errors below.")
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
        try:
            player.delete()
            messages.success(request, "Player deleted successfully.")
        except IntegrityError:
            messages.error(request, "Cannot delete this player because it is referenced in another table.")
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
        try:
            club.delete()
            messages.success(request, "Club deleted successfully.")
        except IntegrityError:
            messages.error(request, "Cannot delete this club because it is referenced in another table.")
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

def club_detail(request, club_id):
    club = get_object_or_404(Clubs, id=club_id)
    players = Players.objects.filter(current_club = club_id)
    

    players_dist = {} 

    for player in players:
        positions = Positions.objects.filter(
            id__in=PlayersPositions.objects.filter(players_id=player.id).values_list('positions_id', flat=True)
        )  

        if player.id not in players_dist:
            players_dist[player.id] = {'player': player, 'positions': positions} 

    matches = Matches.objects.filter(home_club=club_id) | Matches.objects.filter(away_club=club_id)

    return render(request, 'myapp/details/club_detail.html', {'club': club, 'matches': matches, 'players': players_dist})

def player_detail(request, player_id):
    player = get_object_or_404(Players, id=player_id)
    positions = Positions.objects.filter(id__in=PlayersPositions.objects.filter(players_id=player.id).values_list('positions_id', flat=True))

    return render(request, 'myapp/details/player_detail.html', {'players': player, 'positions': positions})

def check_ban(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            profile = Profile.objects.get(user=request.user)
            if profile.is_banned:
                return redirect('main_page')
        return view_func(request, *args, **kwargs)
    return wrapper

@check_ban
@login_required
def toggle_favorite_match(request, match_id):
    if request.user.is_superuser:
        return JsonResponse({'status': 'error', 'message': 'Admins cannot modify favorites.'})

    match = get_object_or_404(Matches, id=match_id)
    favorite, created = FavoriteMatch.objects.get_or_create(user=request.user, match=match)

    if not created:
        favorite.delete()
        return JsonResponse({'status': 'removed'})
    return JsonResponse({'status': 'added'})


@user_passes_test(lambda u: u.is_superuser)
def toggle_ban(request, user_id):
    user = get_object_or_404(User, id=user_id)
    profile, created = Profile.objects.get_or_create(user=user)
    profile.is_banned = not profile.is_banned
    profile.save()
    return redirect('admin_user_favorites')

@user_passes_test(lambda u: u.is_superuser)
def admin_user_favorites(request):
    users = User.objects.filter(is_superuser=False)
    favorites_by_user = {}

    for user in users:
        favorite_matches = FavoriteMatch.objects.filter(user=user).select_related('match')
        favorites_by_user[user] = [f.match for f in favorite_matches]

    return render(request, 'myapp/user_favorites.html', {
        'favorites_by_user': favorites_by_user
    })

@login_required
def my_account(request):
    user = request.user
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')

        if name:
            user.username = name
        if email:
            user.email = email
        user.save()

        # Пароль (через окрему форму)
        password_form = PasswordChangeForm(user, request.POST)
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            messages.success(request, "Profile updated successfully.")
        else:
            if request.POST.get('old_password'):
                messages.error(request, "Password change failed. Check your inputs.")
    else:
        password_form = PasswordChangeForm(user)

    favorites = FavoriteMatch.objects.filter(user=user).select_related('match')
    return render(request, 'myapp/my_account.html', {
        'user': user,
        'favorites': [f.match for f in favorites],
        'password_form': password_form
    })


@user_passes_test(lambda u: u.is_superuser)
def read_unban_request(request, user_id):
    user = get_object_or_404(User, id=user_id)
    request_text = get_object_or_404(UnbanRequest, user=user)
    return render(request, 'myapp/unban_request.html', {
        'user_obj': user,
        'message': request_text.message,
        'created': request_text.created_at
    })

