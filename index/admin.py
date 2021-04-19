from django.contrib import admin
from .models import Tags, Post, Comments, LikesUsers

admin.site.register(Post)
admin.site.register(Tags)
admin.site.register(Comments)
admin.site.register(LikesUsers)
