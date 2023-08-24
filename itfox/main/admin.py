from django.contrib import admin

from .models import Comment, News, Like


class CommentAdmin(admin.ModelAdmin):
    """ Comment admin model. """

    list_display = (
        'author',
        'get_text',
        'published_at',
    )
    list_filter = (
        'published_at',
    )
    search_fields = (
        'text',
    )

    @admin.display(description='Text')
    def get_text(self, obj):
        return obj.text[:25]


class NewsAdmin(admin.ModelAdmin):
    """ News admin model. """

    list_display = (
        'author',
        'header',
        'published_at',
    )
    list_filter = (
        'published_at',
    )
    list_editable = (
        'header',
    )
    search_fields = (
        'text',
    )


admin.site.register(Comment, CommentAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Like)
