from django.contrib import admin
from .models import Tags, Post, Comments, LikesUsers, ViewedPost

admin.site.register(Post)
admin.site.register(Tags)
admin.site.register(Comments)
admin.site.register(LikesUsers)
admin.site.register(ViewedPost)
