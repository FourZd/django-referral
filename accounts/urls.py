# accounts/urls.py
from django.urls import path
from .views import RequestCodeView, VerifyCodeView, UserProfileView, ActivateInviteView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('auth/request_code', RequestCodeView.as_view(), name='request_code'),
    path('auth/verify_code', VerifyCodeView.as_view(), name='verify_code'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('profile', UserProfileView.as_view(), name='user_profile'),
    path('profile/activate_invite', ActivateInviteView.as_view(), name='activate_invite'),
]