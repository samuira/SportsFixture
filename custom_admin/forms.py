from django import forms
from django.db.models import Q
from cricket_app.models import Player, Team, Fixture, Match
from django.utils.translation import ugettext_lazy as _


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(max_length=32, widget=forms.PasswordInput)


class PlayerCreateForm(forms.Form):
    image_uri = forms.ImageField(required=False)
    first_name = forms.CharField(max_length=300, required=True)
    last_name = forms.CharField(max_length=300, required=True)
    jersey_number = forms.IntegerField(max_value=11, min_value=1, required=True)
    country = forms.CharField(max_length=250, required=True)

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        if Player.objects.filter(Q(first_name=first_name) & Q(last_name=last_name)).exists():
            raise forms.ValidationError(
                _('A Player with same Name have already existed.'),
                code='name', )
        return self.cleaned_data


class PlayerEditForm(PlayerCreateForm):

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(PlayerEditForm, self).__init__(*args, **kwargs)

    def clean(self):
        first_name = self.cleaned_data.get('first_name')
        last_name = self.cleaned_data.get('last_name')
        if Player.objects.filter(Q(first_name=first_name) & Q(last_name=last_name)).exclude(pk=self.pk).exists():
            raise forms.ValidationError(
                _('A Player with same Name have already existed.'),
                code='name', )
        return self.cleaned_data


class TeamCreateForm(forms.Form):
    logoUri = forms.ImageField(required=False)
    name = forms.CharField(max_length=300, required=True)
    club_state = forms.CharField(max_length=300, required=True)
    players = forms.MultipleChoiceField(choices=Player.objects.all().values_list('id', 'first_name'), required=False)

    def clean(self):
        name = self.cleaned_data.get('name')
        if Team.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError(
                _('A Player with same Name have already existed.'),
                code='name', )
        return self.cleaned_data


class TeamEditForm(TeamCreateForm):

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(TeamEditForm, self).__init__(*args, **kwargs)

    def clean(self):
        name = self.cleaned_data.get('name')
        if Team.objects.filter(name__iexact=name).exclude(pk=self.pk).exists():
            raise forms.ValidationError(
                _('A Team with same Name have already existed.'),
                code='name', )
        return self.cleaned_data


class FixtureCreateForm(forms.Form):
    name = forms.CharField(max_length=300, required=True)
    teams = forms.MultipleChoiceField(choices=Team.objects.all().values_list('id', 'name'), required=True)


class FixtureEditForm(forms.Form):
    winner = forms.ChoiceField(choices=Team.objects.all().values_list('id', 'name'), required=True)
    score_team1 = forms.IntegerField(required=True)
    score_team2 = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(FixtureEditForm, self).__init__(*args, **kwargs)


class PlayerHistoryEditForm(forms.Form):
    run = forms.IntegerField(required=True)

    def __init__(self, *args, **kwargs):
        self.pk = kwargs.pop('pk', None)
        super(PlayerHistoryEditForm, self).__init__(*args, **kwargs)


