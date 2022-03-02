from django.urls import URLPattern, path
from . import views
from knox import views as knox_views


urlpatterns = [
    path("login/", views.LoginView.as_view()),
    path("user/", views.get_user_data),
    path("register/", views.RegisterView.as_view()),
    path("logout/", knox_views.LogoutView.as_view()),
    path("logoutall/", knox_views.LogoutAllView.as_view()),
    # path("profile/", views.home_profile),
]
