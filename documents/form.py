from django import forms
from .models import Files

class PostForm(forms.ModelForm):

    class Meta:
        model = Files
        fields = ['cover', 'name', 'owner']