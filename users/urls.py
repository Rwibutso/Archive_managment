from django.urls import URLPattern, path, re_path
from . import views


urlpatterns = [
    path("users/", views.UserListView.as_view(), name="rest_user_list"),
    path("user/me/", views.UserDetailsView.as_view(), name="rest_user_details"),
    # Special characters here means regulat expressions as this endpoing needs user's id
    # which are captured by django using regular expressions
    re_path(
        r"^user/(?P<pk>[a-z0-9\-]+)/$", views.UserView.as_view(), name="user_detail"
    ),
]
