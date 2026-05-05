from django.contrib import admin
from .models import Category, Announcement, AnnouncementStatus, Comment, AnnouncementMark, Author

admin.site.site_header = "Elonlar"
admin.site.site_title = "Elon Tv"

# admin.site.login_template = 'login/login.html'
# admin.site.logout_template = 'login/logout.html'

admin.site.register(Category)
admin.site.register(Announcement)
admin.site.register(AnnouncementMark)
admin.site.register(AnnouncementStatus)
admin.site.register(Comment)
admin.site.register(Author)
