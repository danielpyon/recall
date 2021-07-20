from django import forms

from .models import Snippet, Tag

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['code', 'language', 'title', 'starred', 'tags', 'description']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_type']
    