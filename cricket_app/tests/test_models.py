from django.conf import settings
from django.test import TestCase
from cricket_app.models import Player, Team, Match, Fixture, PlayerHistory, Point
from django.core.files.uploadedfile import SimpleUploadedFile


class FixtureTestCase(TestCase):

    def setUp(self):
        self.player1 = Player.objects.create(
            first_name='fn1',
            last_name='ln1',
            image_uri=SimpleUploadedFile(name='viratkohli.jpeg', content=open(settings.MEDIA_ROOT+'/player/image_uri/2020/01/11/viratkohli.jpeg', 'rb').read(), content_type='image/jpeg'),
            jersey_number=1,
            country='india'
        )
        self.player2 = Player.objects.create(
            first_name='fn2',
            last_name='ln2',
            image_uri=SimpleUploadedFile(name='viratkohli.jpeg', content=open(settings.MEDIA_ROOT+'/player/image_uri/2020/01/11/viratkohli.jpeg', 'rb').read(), content_type='image/jpeg'),
            jersey_number=2,
            country='india'
        )

        self.team1 = Team.objects.create(
            name='n1',
            logoUri=SimpleUploadedFile(name='viratkohli.jpeg', content=open(settings.MEDIA_ROOT+'/player/image_uri/2020/01/11/viratkohli.jpeg', 'rb').read(), content_type='image/jpeg'),
            club_state='ct1',
        )
        self.team1.players.add(self.player1)

        self.team2 = Team.objects.create(
            name='n2',
            logoUri=SimpleUploadedFile(name='viratkohli.jpeg', content=open(settings.MEDIA_ROOT+'/player/image_uri/2020/01/11/viratkohli.jpeg', 'rb').read(), content_type='image/jpeg'),
            club_state='ct2',
        )
        self.team2.players.add(self.player2)

        self.fixture = Fixture.objects.create(
            name='fn'
        )
        self.teams = [self.team1, self.team2]
        self.fixture.teams.add(*self.teams)
        while self.teams:
            t1 = self.teams.pop()
            for t2 in self.teams:
                match = Match.objects.create(
                    name='{} VS {}'.format(t1.name, t2.name),
                    team1=t1,
                    team2=t2
                )
                self.fixture.matches.add(match)

        for match in self.fixture.matches.all():
            for player1 in match.team1.players.all():
                PlayerHistory.objects.create(
                    fixture=self.fixture,
                    match=match,
                    team=match.team1,
                    player=player1
                )
            for player2 in match.team2.players.all():
                PlayerHistory.objects.create(
                    fixture=self.fixture,
                    match=match,
                    team=match.team2,
                    player=player2
                )
            Point.objects.create(
                fixture=self.fixture,
                match=match,
                team=match.team1
            )
            Point.objects.create(
                fixture=self.fixture,
                match=match,
                team=match.team2
            )

    def test_number_of_matches(self):
        self.assertEqual(self.fixture.matches.all().count(), 1)

    def test_number_of_players_in_team1(self):
        self.assertEqual(self.team1.players.count(), 1)

    def test_number_of_teams_in_fixture(self):
        self.assertEqual(self.fixture.teams.count(), 2)