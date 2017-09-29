from django.contrib import admin
from news.models import News, Comment, UpVoteCounter


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('news',)
    ordering = ['id']

    def get_actions(self, request):
        # Disable delete
        actions = super(CommentAdmin, self).get_actions(request)
        del actions['delete_selected']
        return actions

    def __init__(self, *args, **kwargs):
        super(CommentAdmin, self).__init__(*args, **kwargs)


admin.site.register(News)
admin.site.register(UpVoteCounter)
admin.site.register(Comment, CommentAdmin)

# Register your models here.
