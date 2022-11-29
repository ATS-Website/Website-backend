from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('admin/login', views.LoginView.as_view(), name='admin-login'),
    path('token/refresh', TokenRefreshView.as_view(), name='token-refresh'),
    path('admin/register', views.RegistrationView.as_view(), name='admin-register'),
    path('ts/register', views.RegistrationView.as_view(), name='ts-register'),



    #     path('verify-email/', views.VerifyEmail.as_view(), name='verify-email'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('change-password/<int:pk>/', views.ChangePasswordAV.as_view(),
         name='change-password'),
    path('forgot-password', views.ForgotPassordAV.as_view(),
         name='forgot-password'),
    path('reset-password/<uuidb64>/<token>/', views.ResetPassordAV.as_view(),
         name='reset-password'),
    path('password-reset-complete/', views.SetNewPasswordAV.as_view(),
         name='password-reset-complete'),

    path('profiles/<int:pk>/',
         views.ProfileRetrieveAPIView.as_view(), name="profile"),
    path('update-profile/<int:pk>/', views.UpdateProfileView.as_view(),
         name='update-profile'),
    path('me/', views.AccountRetrieveUpdateAPIView.as_view(), name='me'),
    path('all', views.AccountsRetrieveAV.as_view(), name='admins'),
    path('toggle-content-manager/<int:pk>', views.ToggleContentManagerAV.as_view(),
         name='toggle-content-manager'),
    path('toggle-membership-manager/<int:pk>',
         views.ToggleMembershipManagerAV.as_view(), name='toggle-membership-manager'),
    path('toggle-assessment-manager/<int:pk>', views.ToggleAssessmentManagerAV.as_view(),
         name='toggle-assessment-manager'),
    path('toggle-application-manager/<int:pk>', views.ToggleApplicationManagerAV.as_view(),
         name='toggle-application-manager'),

]
