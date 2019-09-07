from django.contrib import admin

# Register your models here.
from nfl.models import Team, Game, Player, Selection
 
admin.site.register(Team)
admin.site.register(Game)
admin.site.register(Player)
admin.site.register(Selection)