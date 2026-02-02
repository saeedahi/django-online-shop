from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserPanelDashboardPageView.as_view(), name='user_panel_dashboard_page'),
    path('edit_user_profile', views.EditUserProfilePageView.as_view(), name='edit_user_profile_page'),
    path('change_password', views.ChangePasswordView.as_view(), name='change_password_page'),
    path('register/', views.RegisterView.as_view(), name='register_page'),
    path('activate-account/<email_active_code>/', views.ActiveAccountView.as_view(), name='activate_account'),
    path('login/', views.LoginView.as_view(), name='login_page'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('forgot-password/', views.ForgotPasswordView.as_view(), name='forgot_password_page'),
    path('reset-password/<email_active_code>', views.ResetPasswordView.as_view(), name='reset_password'),
]