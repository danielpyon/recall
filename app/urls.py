from django.urls import path

from . import views

app_name = 'app'

urlpatterns = [
    path('', views.index, name='index'),
    path('snippets/', views.SnippetListView.as_view(), name='snippets'),
    path('snippets/search/<str:query>', views.SnippetSearchListView.as_view(), name='snippet-search'),
    path('snippets/search/advanced/<str:query>', views.SnippetAdvancedSearchListView.as_view(), name='snippet-advanced-search'),
    path('snippets/search/advanced/', views.SnippetAdvancedSearchListView.as_view(), name='snippet-advanced-search'),
    path('snippets/search', views.SnippetSearchListView.as_view(), name='snippet-search'),
    path('snippet/<uuid:pk>', views.SnippetDetailView.as_view(), name='snippet-detail'),
    path('snippet/<uuid:pk>/raw', views.snippet_raw, name='snippet-raw'),
    path('snippet/<uuid:pk>/delete', views.snippet_delete, name='snippet-delete'),
    path('snippet/<uuid:pk>/edit', views.snippet_edit, name='snippet-edit'),
    path('snippet/add', views.snippet_add, name='snippet-add'),
    path('tag/<int:pk>', views.tag, name='tag-detail'),
    path('tag/<int:pk>/delete', views.tag_delete, name='tag-delete'),
    path('tag/add', views.tag_add, name='tag-add'),
    path('tags/', views.TagListView.as_view(), name='tags'),
    path('tags/<int:pk>/edit', views.tag_edit , name='tag-edit'),
    path('tags/search/<str:query>', views.TagSearchListView.as_view(), name='tag-search'),
    path('tags/search', views.TagSearchListView.as_view(), name='tag-search'),
    path('languages', views.languages, name='languages'),
    path('settings/', views.settings_view, name='settings'),
]
