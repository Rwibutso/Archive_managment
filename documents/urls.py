from django.urls import path, re_path
from . import views

urlpatterns = [
    path("alldocs/", views.DocListView.as_view(), name="rest_doc_list"),
    path("add_docs/", views.DocUploadView.as_view(), name="rest_doc_create"),
    re_path(r"^doc/(?P<pk>[a-z0-9\-]+)/$", views.DocView.as_view(), name="doc_detail"),
    re_path(
        r"^user/(?P<user_id>[a-z0-9\-]+)/docs/$",
        views.DocListByUserView.as_view(),
        name="user_docs",
    ),
]
