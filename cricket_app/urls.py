from django.urls import path
from .views import *

urlpatterns = [
    path('team_list', TeamListView.as_view(), name='api-team-list'),
    path('player_list', PlayerListView.as_view(), name='api-player-list'),
    path('match_fixture_list', MatchFixtureListView.as_view(), name='api-match-fixture-list'),
]
