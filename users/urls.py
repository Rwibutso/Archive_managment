from django.urls import URLPattern, path, re_path
from . import views


urlpatterns = [
    path("", views.UserListView.as_view(), name="rest_user_list"),
    path("me/", views.UserDetailsView.as_view(), name="rest_user_details"),
    re_path(r"^(?P<pk>[a-z0-9\-]+)/$", views.UserView.as_view(), name="user_detail")
]
