from django.contrib import admin

from .models import Quiz, UserProfile, Question, Option

# Register your models here.
admin.site.register(Option)
admin.site.register(Question)
admin.site.register(Quiz)
admin.site.register(UserProfile)
