from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

import uuid

class Tag(models.Model):
    tag_type = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    class Meta:
        ordering = ['tag_type']

    def get_absolute_url(self):
        return reverse('app:tag-detail', args=[str(self.id)])

    def count(self):
        return Snippet.objects.filter(user=self.user, tags=self).distinct().count()

    def __str__(self):
        return f'Tag "{self.tag_type}"'

class Snippet(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique id for a particular snippet')
    code = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True) # deletes snippet when user is deleted
    language = models.CharField(max_length=100)
    title = models.CharField(max_length=200, default='')
    pub_date = models.DateTimeField('date published', auto_now_add=True, blank=True)
    starred = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ['-pub_date', 'language']

    def loc(self):
        return str(self.code).count('\n') + 1

    def get_absolute_url(self):
        return reverse('app:snippet-detail', args=[str(self.id)])

    def __str__(self):
        return self.title