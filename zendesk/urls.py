from django.urls import path

from . import views, controllers

urlpatterns = [
    path("", views.index, name="index"),
    path("oauth/connect", controllers.zendesk_oauth_connect, name="zendesk_oauth_connect"),
    path("oauth/callback", controllers.zendesk_oauth_callback, name="zendesk_oauth_callback"),
]