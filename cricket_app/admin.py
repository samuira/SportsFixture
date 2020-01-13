from django.contrib import admin
from .models import Player, Team, Match, Point, Fixture, PlayerHistory

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Point)
admin.site.register(Fixture)
admin.site.register(PlayerHistory)
