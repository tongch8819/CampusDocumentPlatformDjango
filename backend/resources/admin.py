from django.contrib import admin
from .models import Tag, Material, Sharing, Favorite, Comment
from users.models import CustomUser

admin.site.register(CustomUser)
admin.site.register(Tag)
admin.site.register(Material)
admin.site.register(Sharing)
admin.site.register(Favorite)
admin.site.register(Comment)