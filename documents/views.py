from .models import Files
from django.views.generic import CreateView 
from django.urls import reverse_lazy 
from .form import PostForm


class CreatePostView(CreateView): 
    model = Files
    form_class = PostForm
    template_name = 'upload.html'
    success_url = reverse_lazy('home')