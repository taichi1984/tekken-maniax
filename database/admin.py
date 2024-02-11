from django.contrib import admin
from .models import State,ThrowTech,HitLevel,Move,MoveType,StatePlayer,StateEnemyGuard,StateEnemyHit,StateEnemyAir,StateEnemyDownHit

# Register your models here.
admin.site.register(State)
admin.site.register(ThrowTech)
admin.site.register(HitLevel)
admin.site.register(Move)
admin.site.register(MoveType)
admin.site.register(StatePlayer)
admin.site.register(StateEnemyGuard)
admin.site.register(StateEnemyHit)
admin.site.register(StateEnemyAir)
admin.site.register(StateEnemyDownHit)