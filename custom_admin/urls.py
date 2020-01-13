from django.urls import path
from .views import (Dashboard, Login, Logout, PlayerList, PlayerCreate, PlayerEdit, TeamList, TeamCreate, TeamEdit,
                    FixtureCreate, FixtureList, FixtureEdit, PlayerHistoryEdit)

urlpatterns = [
    path('', Dashboard.as_view(), name='dashboard'),
    path('login', Login.as_view(), name='login'),
    path('logout', Logout.as_view(), name='logout'),
    path('player_list', PlayerList.as_view(), name='player-list'),
    path('player_create', PlayerCreate.as_view(), name='player-create'),
    path('player_edit/<int:pk>/', PlayerEdit.as_view(), name='player-edit'),
    path('team_list', TeamList.as_view(), name='team-list'),
    path('team_create', TeamCreate.as_view(), name='team-create'),
    path('team_edit/<int:pk>/', TeamEdit.as_view(), name='team-edit'),
    path('fixture_create/', FixtureCreate.as_view(), name='fixture-create'),
    path('fixture_list', FixtureList.as_view(), name='fixture-list'),
    path('fixture_edit/<int:pk>/', FixtureEdit.as_view(), name='fixture-edit'),
    path('player_history_edit/<int:pk>/', PlayerHistoryEdit.as_view(), name='player-history-edit'),
]
