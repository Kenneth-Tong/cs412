from django import forms
from .models import Article, Comment

class CreateArticleForm(forms.ModelForm):
    '''A form to add a new Article to the database.'''

    class Meta:
        '''Associate this form with the Article model; select fields to add.'''
        model = Article
        # fields = ['author', 'title', 'text', 'image_url']
        fields = ['author', 'title', 'text', 'image_file']

class UpdateArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'text']

class CreateCommentForm(forms.ModelForm):
    '''A form to add a Comment to the database.'''

    class Meta:
        '''associate this form with the Comment model; select fields'''
        model = Comment
        fields = ['author', 'text']  # which fields from model should we use
