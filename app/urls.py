from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('snippets/', views.SnippetListView.as_view(), name='snippets'),
    path('snippet/<uuid:pk>', views.SnippetDetailView.as_view(), name='snippet-detail'),
    path('snippet/<uuid:pk>/raw', views.snippet_raw, name='snippet-raw'),
    path('snippet/<uuid:pk>/delete', views.snippet_delete, name='snippet-delete'),
    path('snippet/<uuid:pk>/edit', views.snippet_edit, name='snippet-edit'),
    path('snippet/add', views.snippet_add, name='snippet-add'),
    path('tag/<int:pk>', views.tag, name='tag-detail'),
    path('tag/<int:pk>/delete', views.tag_delete, name='tag-delete'),
    path('tag/add', views.tag_add, name='tag-add'),
    path('tags/', views.TagListView.as_view(), name='tags'),
    path('settings/', views.settings_view, name='settings'),
]
