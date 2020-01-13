from django.views.generic import ListView, DetailView
from cricket_app.models import Fixture, Team, Player


class TeamListViewFE(ListView):
    template_name = 'custom_admin/frontend/team_list.html'
    queryset = Fixture.objects.all().first().teams.all()
    context_object_name = 'teams'


class TeamDetailViewFE(DetailView):
    template_name = 'custom_admin/frontend/team_details.html'
    model = Team
    context_object_name = 'team'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PlayerListViewFE(ListView):
    template_name = 'custom_admin/frontend/player_list.html'
    queryset = Player.objects.all()
    context_object_name = 'players'


class FixtureListViewFE(ListView):
    template_name = 'custom_admin/frontend/fixture_list.html'
    queryset = Fixture.objects.all().first().matches.all() if Fixture.objects.all().first() else None
    context_object_name = 'matches'
