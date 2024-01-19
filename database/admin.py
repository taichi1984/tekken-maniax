from django.contrib import admin
from .models import State,ThrowTech,HitLevel,Move,MoveType

# Register your models here.
admin.site.register(State)
admin.site.register(ThrowTech)
admin.site.register(HitLevel)
admin.site.register(Move)
admin.site.register(MoveType)