from django.urls import path
from .views import *

urlpatterns = [
    path('', FixtureListViewFE.as_view(), name='fe-fixture-list'),
    path('team_list', TeamListViewFE.as_view(), name='fe-team-list'),
    path('player_list', PlayerListViewFE.as_view(), name='fe-player-list'),
    path('team_details/<slug:pk>/', TeamDetailViewFE.as_view(), name='fe-team-details'),
]
