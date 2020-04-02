from django.contrib import admin
from .models import Guide, Category, Character, GuideComment, Favorite, Evaluation

# Register your models here.
admin.site.register(Guide)
admin.site.register(Category)
admin.site.register(Character)
admin.site.register(GuideComment)
admin.site.register(Favorite)
admin.site.register(Evaluation)
