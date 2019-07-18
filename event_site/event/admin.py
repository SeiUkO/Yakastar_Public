from django.contrib import admin
from .models import Event, Users, Assos, Assos_user

admin.site.register(Event)
admin.site.register(Users)
admin.site.register(Assos)
admin.site.register(Assos_user)
# Register your models here.
