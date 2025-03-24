# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Clubs(models.Model):
    id = models.AutoField(primary_key=True)
    full_title = models.CharField(blank=True, null=True)
    location = models.CharField(blank=True, null=True)
    stadium = models.CharField(blank=True, null=True)
    league = models.ForeignKey('Leagues', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Clubs'
    
    def __str__(self):
        return self.full_title if self.full_title else "Unknown Position"


class Countries(models.Model):
    id = models.AutoField(primary_key=True)
    full_title = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Countries'
    
    def __str__(self):
        return self.full_title if self.full_title else "Unknown Position"


class Leagues(models.Model):
    id = models.AutoField(primary_key=True)
    full_title = models.CharField(blank=True, null=True)
    country = models.ForeignKey(Countries, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Leagues'
    
    def __str__(self):
        return self.full_title if self.full_title else "Unknown Position"


class Matches(models.Model):
    id = models.AutoField(primary_key=True)
    home_club = models.ForeignKey(Clubs, models.DO_NOTHING, blank=True, null=True)
    away_club = models.ForeignKey(Clubs, models.DO_NOTHING, related_name='matches_away_club_set', blank=True, null=True)
    home_goals = models.IntegerField(blank=True, null=True)
    away_goals = models.IntegerField(blank=True, null=True)
    date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Matches'



class Players(models.Model):
    id = models.AutoField(primary_key=True)
    player_name = models.CharField(blank=True, null=True)
    birthday = models.DateField(blank=True, null=True)
    current_club = models.ForeignKey(Clubs, models.DO_NOTHING, blank=True, null=True)
    country = models.ForeignKey(Countries, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Players'
    
    def __str__(self):
        return self.player_name if self.player_name else "Unnamed Player"


class PlayersPositions(models.Model):
    players = models.ForeignKey(Players, on_delete=models.PROTECT, db_column='Players_id')  # Field name made lowercase.
    positions = models.ForeignKey('Positions', on_delete=models.PROTECT, db_column='Positions_id')  # Field name made lowercase.

    class Meta:
        unique_together = ('players', 'positions')
        db_table = 'Players_Positions'
        managed = False


class Positions(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Positions'
    
    def __str__(self):
        return self.title if self.title else "Unknown Position"


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'

