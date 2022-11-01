from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('admin/login', views.LoginView.as_view(), name='admin-login'),
    # path('ts/login', views.LoginView.as_view(), name='ts-login'),
    # path('applicant/login', views.LoginView.as_view(), name='applicant-login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('admin/register', views.RegistrationView.as_view(), name='admin-register'),
    path('ts/register', views.RegistrationView.as_view(), name='ts-register'),
    # path('applicant/register', views.ApplicantRegistrationAV.as_view(),
    #      name='applicant-register'),



    path('verify-email/', views.VerifyEmail.as_view(), name='verify-email'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change-password/<int:pk>/', views.ChangePasswordAV.as_view(),
         name='change-password'),
    path('forgot-password/<int:pk>/', views.ForgotPassordAV.as_view(),
         name='forgot-password'),
    path('reset-password/<int:uuidb64>/<token>/', views.ResetPassordAV.as_view(),
         name='reset-password'),
    path('password-reset-complete/', views.SetNewPasswordAV.as_view(),
         name='password-reset-complete'),

    path('users/', views.AccountsRetrieveAV.as_view(), name='users'),
    # path('', views.GetRouteAV.as_view(), name='get-routes'),
]
