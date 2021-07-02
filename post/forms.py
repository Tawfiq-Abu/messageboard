from django import forms
from django.forms import fields
from . import models

class PostForm(forms.ModelForm):
    class Meta:
        models = models.Post 
        fields = ('author','title','text')



class CommentForm(forms.ModelForm):

    class Meta:
        model = models.Comment
        fields = ('author', 'text',)