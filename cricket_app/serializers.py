from rest_framework import serializers
from cricket_app.models import Player, Team, Match


class PlayerListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ('image_uri', 'last_name', 'first_name', )


class TeamListSerializer(serializers.ModelSerializer):
    players = PlayerListSerializer(many=True)

    class Meta:
        model = Team
        fields = ('logoUri', 'name', 'players', 'total_point', )


class MatchFixtureListSerializer(serializers.ModelSerializer):
    team1 = TeamListSerializer()
    team2 = TeamListSerializer()
    winner = TeamListSerializer()

    class Meta:
        model = Match
        fields = ('name', 'team1', 'team2', 'winner', )