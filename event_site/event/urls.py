from django.urls import path

from . import views
from .models import EventForm
from .views import logged


urlpatterns = [
        path('form/', EventForm.as_view(), name = 'event'),
        path('', logged, name = 'index'),
        path('home/', logged, name='logged'),
        path('homes/', views.logged_after_passphrase),
        path('passphrase/', views.get_passphrase),
       ]
