from django.urls import path, re_path
from . import views


urlpatterns = [
    path("allusers/", views.UserListView.as_view(), name="rest_user_list"),
    path("me/", views.UserDetailsView.as_view(), name="rest_user_details"),
    # Special characters here means regulat expressions as this endpoing needs user's id
    # which are captured by django using regular expressions
    # path(
    #     "user/", views.UserView.as_view(), name="user_detail"
    # ),
    re_path(
        r"^user/(?P<pk>[a-z0-9\-]+)/$", views.UserView.as_view(), name="user_detail"
    ),
]
