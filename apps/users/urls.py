from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import MeView, TelegramAuthStartView, TelegramAuthStatusView, TelegramLoginView, TelegramWebhookView

urlpatterns = [
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("telegram/login/", TelegramLoginView.as_view(), name="telegram-login"),
    path("telegram/auth/start/", TelegramAuthStartView.as_view(), name="telegram-auth-start"),
    path("telegram/auth/status/<str:token>/", TelegramAuthStatusView.as_view(), name="telegram-auth-status"),
    path("telegram/webhook/", TelegramWebhookView.as_view(), name="telegram-webhook"),
    path("me/", MeView.as_view(), name="me"),
]
