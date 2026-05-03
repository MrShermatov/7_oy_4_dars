from django.contrib import admin
from .models import Category, Announcement, AnnouncementStatus, Comment, AnnouncementMark, Author

admin.site.register(Category)
admin.site.register(Announcement)
admin.site.register(AnnouncementMark)
admin.site.register(AnnouncementStatus)
admin.site.register(Comment)
admin.site.register(Author)
