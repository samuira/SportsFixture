from django.views.generic import ListView
from rest_framework.authentication import BasicAuthentication
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny
from cricket_app.csrf_exempt import CsrfExemptSessionAuthentication
from cricket_app.models import Fixture, Team, Player
from cricket_app.serializers import TeamListSerializer, PlayerListSerializer, MatchFixtureListSerializer
from rest_framework import generics


class TeamListView(generics.ListCreateAPIView):
    parser_classes = (JSONParser, )
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication,)
    queryset = Fixture.objects.all().first().teams.all()
    serializer_class = TeamListSerializer


class PlayerListView(generics.ListCreateAPIView):
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication,)
    queryset = Player.objects.all()
    serializer_class = PlayerListSerializer


class MatchFixtureListView(generics.ListCreateAPIView):
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication,)
    queryset = Fixture.objects.all().first().matches.all()
    serializer_class = MatchFixtureListSerializer


class PointListView(generics.ListCreateAPIView):
    parser_classes = (JSONParser,)
    permission_classes = (AllowAny,)
    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication,)
    queryset = Fixture.objects.all().first().matches.all()
    serializer_class = MatchFixtureListSerializer






