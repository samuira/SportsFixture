from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView
from cricket_app.models import Player, Team, Fixture, Match, PlayerHistory, Point
from custom_admin.utils import Util
from .forms import LoginForm, PlayerCreateForm, PlayerEditForm, TeamCreateForm, TeamEditForm, FixtureCreateForm, \
    FixtureEditForm, PlayerHistoryEditForm
from django.shortcuts import redirect


class Dashboard(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'custom_admin/dashboard.html'
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')

    def get(self, request):
        return render(request, self.template_name)


class Login(View):
    template_name = 'custom_admin/account/login.html'
    form_class = LoginForm
    context = dict()

    def get(self, request, *args, **kwargs):
        self.context.clear()
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        self.context.clear()
        form = self.form_class(request.POST)
        self.context['form'] = form
        if form.is_valid():
            user = authenticate(request=request, email=request.POST['email'], password=request.POST['password'])
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.error(request, 'Incorrect Email or Password')
        else:
            error = Util.form_validation_error(request, form)
            self.context['error'] = error
        return render(request, self.template_name, self.context)


class Logout(LoginRequiredMixin, UserPassesTestMixin, View):
    login_url = reverse_lazy('login')

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('login'))


class PlayerList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'custom_admin/player/list.html'
    login_url = reverse_lazy('login')
    queryset = Player.objects.all()
    paginate_by = 10
    context_object_name = 'players'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')


class PlayerCreate(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'custom_admin/player/create.html'
    login_url = reverse_lazy('login')
    form_class = PlayerCreateForm
    context = dict()

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')

    def get(self, request):
        self.context.clear()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        self.context.clear()
        form = self.form_class(request.POST, request.FILES)
        self.context['form'] = form
        if form.is_valid():
            print(form.cleaned_data)
            Player.objects.create(
                first_name=form.cleaned_data.get('first_name', ''),
                last_name=form.cleaned_data.get('last_name', ''),
                image_uri=form.cleaned_data.get('image_uri', ''),
                jersey_number=form.cleaned_data.get('jersey_number', 0),
                country=form.cleaned_data.get('country')
            )
            messages.success(self.request, 'Player has been created successfully.')
            return HttpResponseRedirect(reverse('player-list'))
        else:
            error = Util.form_validation_error(request, form)
            self.context['error'] = error
        return render(request, self.template_name, self.context)


class PlayerEdit(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'custom_admin/player/edit.html'
    login_url = reverse_lazy('login')
    form_class = PlayerEditForm
    context = dict()

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')

    def get(self, request, **kwargs):
        self.context['player'] = Player.objects.get(pk=kwargs['pk'])
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, pk=self.context['player'].id)
        self.context['form'] = form
        if form.is_valid():
            print(form.cleaned_data)
            player = self.context['player']
            player.image_uri = form.cleaned_data.get('image_uri', '') or player.image_uri
            player.first_name = form.cleaned_data.get('first_name')
            player.last_name = form.cleaned_data.get('last_name')
            player.jersey_number = form.cleaned_data.get('jersey_number')
            player.country = form.cleaned_data.get('country')
            player.save()
            messages.success(self.request, 'Player has been updated successfully.')
            return HttpResponseRedirect(reverse('player-list'))
        else:
            error = Util.form_validation_error(request, form)
            self.context['error'] = error
        return render(request, self.template_name, self.context)


class TeamList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'custom_admin/team/list.html'
    login_url = reverse_lazy('login')
    queryset = Team.objects.all()
    paginate_by = 10
    context_object_name = 'teams'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')


class TeamCreate(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'custom_admin/team/create.html'
    login_url = reverse_lazy('login')
    form_class = TeamCreateForm
    context = dict()

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')

    def get(self, request):
        self.context.clear()
        selected_player_ids = [player.id for team in Team.objects.all() for player in team.players.all()]
        print(selected_player_ids)
        self.context['players'] = Player.objects.exclude(id__in=selected_player_ids)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        self.context.clear()
        form = self.form_class(request.POST, request.FILES)
        self.context['form'] = form
        if form.is_valid():
            print(form.cleaned_data)
            team = Team.objects.create(
                name=form.cleaned_data.get('name', ''),
                logoUri=form.cleaned_data.get('logoUri', ''),
                club_state=form.cleaned_data.get('club_state', ''),
            )
            player_ids = form.cleaned_data['players']
            players = [player for player in Player.objects.filter(pk__in=player_ids)]
            team.players.add(*players)
            messages.success(self.request, 'Team has been created successfully.')
            return HttpResponseRedirect(reverse('team-list'))
        else:
            error = Util.form_validation_error(request, form)
            self.context['error'] = error
        return render(request, self.template_name, self.context)


class TeamEdit(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'custom_admin/team/edit.html'
    login_url = reverse_lazy('login')
    form_class = TeamEditForm
    context = dict()

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')

    def get(self, request, **kwargs):
        self.context['team'] = Team.objects.get(pk=kwargs['pk'])
        selected_player_ids = [player.id for team in Team.objects.exclude(id=int(kwargs['pk'])) for player in team.players.all()]
        print(selected_player_ids)
        self.context['players'] = Player.objects.exclude(id__in=selected_player_ids)
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, pk=self.context['team'].id)
        self.context['form'] = form
        print(form.is_valid())
        if form.is_valid():
            print(form.cleaned_data)
            print(form.cleaned_data['players'])
            team = self.context['team']
            team.logoUri = form.cleaned_data.get('logoUri', '') or team.logoUri
            team.name = form.cleaned_data.get('name')
            team.club_state = form.cleaned_data.get('club_state')
            team.players.clear()
            player_ids = form.cleaned_data['players']
            players = [player for player in Player.objects.filter(pk__in=player_ids)]
            team.players.add(*players)
            team.save()
            messages.success(self.request, 'Team has been updated successfully.')
            return HttpResponseRedirect(reverse('team-list'))
        else:
            error = Util.form_validation_error(request, form)
            print(error)
            self.context['error'] = error
        return render(request, self.template_name, self.context)


class FixtureList(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'custom_admin/fixture/list.html'
    login_url = reverse_lazy('login')
    queryset = Match.objects.all()
    paginate_by = 10
    context_object_name = 'matches'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')


class FixtureCreate(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'custom_admin/fixture/create.html'
    login_url = reverse_lazy('login')
    form_class = FixtureCreateForm
    context = dict()

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')

    def get(self, request):
        self.context.clear()
        self.context['teams'] = Team.objects.all()
        return render(request, self.template_name, self.context)

    @staticmethod
    def reset_fixture():
        fd = Fixture.objects.all()
        for f in fd:
            f.matches.clear()
            f.teams.clear()
        md = Match.objects.all()
        phd = PlayerHistory.objects.all()
        pd = Point.objects.all()
        fd.delete()
        md.delete()
        phd.delete()
        pd.delete()

    @staticmethod
    def create_player_history(fixture):
        for match in fixture.matches.all():
            for player1 in match.team1.players.all():
                PlayerHistory.objects.create(
                    fixture=fixture,
                    match=match,
                    team=match.team1,
                    player=player1
                )
            for player2 in match.team2.players.all():
                PlayerHistory.objects.create(
                    fixture=fixture,
                    match=match,
                    team=match.team2,
                    player=player2
                )
            Point.objects.create(
                fixture=fixture,
                match=match,
                team=match.team1
            )
            Point.objects.create(
                fixture=fixture,
                match=match,
                team=match.team2
            )

    @staticmethod
    def create_fixture(isCreated, fixture, teams):
        if isCreated:
            teams = [team for team in teams]
            fixture.teams.add(*teams)
            while teams:
                team1 = teams.pop()
                for team2 in teams:
                    match = Match.objects.create(
                        name='{} VS {}'.format(team1.name, team2.name),
                        team1=team1,
                        team2=team2
                    )
                    fixture.matches.add(match)

    def post(self, request, *args, **kwargs):
        self.context.clear()
        form = self.form_class(request.POST, request.FILES)
        self.context['form'] = form
        if form.is_valid():
            print(form.cleaned_data)
            self.reset_fixture()
            fixture, isCreated = Fixture.objects.get_or_create(
                name=form.cleaned_data.get('name', '')
            )
            teams = Team.objects.filter(pk__in=form.cleaned_data['teams'])
            self.create_fixture(isCreated, fixture, teams)
            self.create_player_history(fixture)
            messages.success(self.request, 'Fixture has been created successfully.')
            return HttpResponseRedirect(reverse('fixture-list'))
        else:
            error = Util.form_validation_error(request, form)
            self.context['error'] = error
        return render(request, self.template_name, self.context)


class FixtureEdit(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'custom_admin/fixture/edit.html'
    login_url = reverse_lazy('login')
    form_class = FixtureEditForm
    context = dict()

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')

    def get(self, request, **kwargs):
        match = Match.objects.get(pk=kwargs['pk'])
        self.context['match'] = match
        self.context['team1'] = PlayerHistory.objects.filter(Q(match=match) & Q(team=match.team1))
        self.context['team2'] = PlayerHistory.objects.filter(Q(match=match) & Q(team=match.team2))
        self.context['point_team1'] = Point.objects.filter(Q(match=match) & Q(team=match.team1)).first()
        self.context['point_team2'] = Point.objects.filter(Q(match=match) & Q(team=match.team2)).first()
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, pk=self.context['match'].id)
        self.context['form'] = form
        print(form.is_valid())
        if form.is_valid():
            match = self.context['match']
            match.winner = Team.objects.get(pk=form.cleaned_data.get('winner'))
            match.save()
            point_team1 = self.context['point_team1']
            point_team2 = self.context['point_team2']
            point_team1.score = form.cleaned_data.get('score_team1')
            point_team2.score = form.cleaned_data.get('score_team2')
            point_team1.save()
            point_team2.save()
            messages.success(self.request, 'Match has been updated successfully.')
            return HttpResponseRedirect(reverse('fixture-list'))
        else:
            error = Util.form_validation_error(request, form)
            print(error)
            self.context['error'] = error
        return render(request, self.template_name, self.context)


class PlayerHistoryEdit(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'custom_admin/player_history/edit.html'
    login_url = reverse_lazy('login')
    form_class = PlayerHistoryEditForm
    context = dict()

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        messages.error(self.request, 'Permission denied!!!')
        return redirect('login')

    def get(self, request, **kwargs):
        player_history = PlayerHistory.objects.get(pk=kwargs['pk'])
        self.context['player_history'] = player_history
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES, pk=self.context['player_history'].id)
        self.context['form'] = form
        print(form.is_valid())
        if form.is_valid():
            player_history = self.context['player_history']
            player_history.run = form.cleaned_data.get('run')
            player_history.save()
            messages.success(self.request, 'Player run has been updated successfully.')
            return HttpResponseRedirect(reverse('fixture-edit', kwargs={'pk': player_history.match.id}))
        else:
            error = Util.form_validation_error(request, form)
            print(error)
            self.context['error'] = error
        return render(request, self.template_name, self.context)

