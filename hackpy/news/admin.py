from django.contrib import admin
from news.models import News, Comment


class CommentAdmin(admin.ModelAdmin):
    list_filter = ('news',)

admin.site.register(News)
admin.site.register(Comment, CommentAdmin)



# Register your models here.
