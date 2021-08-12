from django import forms
from django.core.exceptions import ValidationError

from .models import Snippet, Tag

class SnippetForm(forms.ModelForm):
    class Meta:
        model = Snippet
        fields = ['code', 'language', 'title', 'starred', 'tags', 'description']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_type']
    def clean(self):
        cd = self.cleaned_data

        if len(Tag.objects.filter(tag_type=cd['tag_type'])) >= 1:
            raise ValidationError('Tag already exists')

        return cd