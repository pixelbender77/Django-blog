from django.contrib import admin
from blog.models import Post, Comment , Like

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)

# Register your models here.
