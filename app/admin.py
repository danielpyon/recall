from django.contrib import admin

from .models import Tag, Snippet

class TagInline(admin.TabularInline):
    model = Snippet.tags.through
    extra = 3

@admin.register(Snippet)
class SnippetAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {
            'fields': [
                'title',
                'code',
                'language',
                'description',
                'starred',
                'user']
        }),
        ('Date information', {
            'fields': ['pub_date'],
            'classes': ['collapse']
        }),
    ]
    inlines = [TagInline]
    save_as = True

admin.site.register(Tag)