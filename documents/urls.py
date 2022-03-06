from django.urls import path
from .import views 



urlpatterns = [
    path('', views.CreatePostView.as_view(), name='home'),
]