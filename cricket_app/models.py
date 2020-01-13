from django.db import models
import uuid
from django.db.models import Sum


class Player(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=250, blank=False)
    last_name = models.CharField(max_length=250, blank=False)
    image_uri = models.ImageField(upload_to='player/image_uri/%Y/%m/%d', blank=False)
    jersey_number = models.PositiveSmallIntegerField()
    country = models.CharField(max_length=250)

    def __str__(self):
        return 'uuid: {}, name: {} {}, jersey number: {}'\
            .format(self.uuid, self.first_name, self.last_name, self.jersey_number)

    def player_high_score(self):
        return PlayerHistory.objects.filter(player=self).order_by('-run').first().run if PlayerHistory.objects.filter(player=self).order_by('-run').first() else 0

    def player_fifties(self):
        return PlayerHistory.objects.filter(player=self).filter(run__gte=50).count()

    def player_hundreds(self):
        return PlayerHistory.objects.filter(player=self).filter(run__gte=100).count()


class Team(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, blank=False)
    logoUri = models.ImageField(upload_to='team/logo_uri/%Y/%m/%d', blank=False)
    club_state = models.CharField(max_length=250, blank=True)
    players = models.ManyToManyField(Player)

    def __str__(self):
        return 'uuid: {}, name: {}'.format(self.uuid, self.name)

    def total_point(self):
        return sum(point.score for point in Point.objects.filter(team=self))


class Match(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, blank=False)
    team1 = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='fkr_team1')
    team2 = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='fkr_team2')
    winner = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, related_name='fkr_winner')

    def __str__(self):
        return 'uuid: {}, name: {}'.format(self.uuid, self.name)


class Fixture(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=250, blank=False)
    matches = models.ManyToManyField(Match)
    teams = models.ManyToManyField(Team)

    def __str__(self):
        return 'uuid: {}, name: {}'.format(self.uuid, self.name)


class Point(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.SET_NULL, null=True)
    match = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True, related_name='r_match')
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    score = models.IntegerField(default=0)

    def __str__(self):
        return 'match: {}, team: {}, score: {}'.format(self.match, self.team, self.score)


class PlayerHistory(models.Model):
    fixture = models.ForeignKey(Fixture, on_delete=models.SET_NULL, null=True)
    match = models.ForeignKey(Match, on_delete=models.SET_NULL, null=True)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True)
    player = models.ForeignKey(Player, on_delete=models.SET_NULL, null=True)
    run = models.IntegerField(default=0)

    def __str__(self):
        return 'name: {} {}, run: {}'\
            .format(self.player.first_name if self.player else '',
                    self.player.last_name if self.player else '', self.run)

    def player_high_score(self):
        return PlayerHistory.objects.filter(player=self.player).order_by('-run').first().run if PlayerHistory.objects.filter(player=self).order_by('-run').first() else 0

    def player_fifties(self):
        return PlayerHistory.objects.filter(player=self.player).filter(run__gte=50).count()

    def player_hundreds(self):
        return PlayerHistory.objects.filter(player=self.player).filter(run__gte=100).count()
