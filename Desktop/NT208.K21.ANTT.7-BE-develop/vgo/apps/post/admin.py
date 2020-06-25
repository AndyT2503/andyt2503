from django.contrib import admin

# Register your models here.
from vgo.apps.post.models import Post
from vgo.apps.post.models import Comment

admin.site.register(Post)
admin.site.register(Comment)