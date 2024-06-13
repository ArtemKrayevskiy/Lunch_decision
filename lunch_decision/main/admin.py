from django.contrib import admin
from .models import User, Restaurant, Menu, Vote
# Register your models here.

admin.site.register(User)
admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Vote)