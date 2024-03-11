from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, controllers

router = DefaultRouter()
router.register(r'tickets', views.TicketViewSet)
router.register(r'daily-ticket-count', views.DailyTicketCountViewSet)

urlpatterns = [
    path("", views.index, name="index"),
    path("oauth/connect", controllers.zendesk_oauth_connect, name="zendesk_oauth_connect"),
    path("oauth/callback", controllers.zendesk_oauth_callback, name="zendesk_oauth_callback"),
    path('api/', include(router.urls)),
]