"""event_site URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

from social_django.urls import urlpatterns as social_django_urls
from .views import EventDetailView
# from django.contrib.auth import logout

urlpatterns = [
    path('event/', include('event.urls')),
    path('admin/', admin.site.urls),
    path('assos/', views.assos, name='assos'),
    path('event_detail/<int:pk>', EventDetailView.as_view(), name='event-detail'),
    path('membres/', views.membres, name='membres'),
    path('events/', views.events, name='events'),
    path('profile/', views.profile_page, name='profile'),
    path('forms/', views.forms, name='forms'),

    path('', include((social_django_urls, "social_django"), namespace='social')),
    path('logout/', views.logout_view, name="logout"),
    path('assos/<int:pk>/', views.AssosDetail.as_view(), name='asso-detail'),
    path('', views.home, name='home'),
    path('form_pdf/<int:pk>', views.GeneratePDF.as_view(), name='gen'),
    path('events/<int:pk>', views.validate_event, name='validate'),

]
urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)