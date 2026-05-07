from django.contrib import admin
from django.utils.safestring import mark_safe
from django.db import models
from django import forms

from .models import Category, Announcement, AnnouncementStatus, Comment, AnnouncementMark, Author

admin.site.site_header = "Elonlar"
admin.site.site_title = "Elon Tv"

# admin.site.login_template = 'login/login.html'
# admin.site.logout_template = 'login/logout.html'

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    exclude = ('user',)
    readonly_fields = ('edited',)
    formfield_overrides = {
        models.TextField:{
            'widget': forms.Textarea(attrs={
                'row': 3,
                'cols': 50,
            })
        }
    }

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'category', 'number', 'location', 'is_active',
                    'get_image', 'get_video']
    list_display_links = ('name',)
    list_filter = ['category', 'is_active' ,'location',]
    list_editable = ['category', 'location']
    search_fields = ['category__name', 'location', 'price']
    list_per_page = 10
    search_help_text = "Nom, narxi yoki manzil bo'yicha qidiring"
    readonly_fields = ['views']
    inlines = [
        CommentInline
    ]
    fieldsets = [
        ('Asosiy', {
            'fields': ['name', 'description']
        }),
        ('Narxlar va aloqa', {
            'fields': ['price', 'number'],
            'description': 'Narxlar uchun'
        }),
        ('Medialar', {
            'fields': ['video', 'image']
        }),
        ('Boshqa ma\'lumotlar', {
            'fields': ['location', 'author', 'views']
        }),
    ]

    @admin.display(description='Rasmi')
    def get_image(self, announcement):
        if announcement.image:
            return mark_safe(f"<img src='{announcement.image.url}' width='150px' style='border-radius: 10px'>")
        else:
            return '-'

    @admin.display(description='Video')
    def get_video(self, obj):
        if obj.video:
            return mark_safe(f"<video src='{obj.video.url}' width='300' controls></video>")
        return '-'

    def save_formset(self, request, form, formset, change):
        instances = formset.save(commit=False)
        for obj in instances:
            if not obj.user:
                obj.user = request.user
            obj.save()
        formset.save_m2m()

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

@admin.register(AnnouncementMark)
class AnnouncementMarkAdmin(admin.ModelAdmin):
    pass

@admin.register(AnnouncementStatus)
class AnnouncementStatusAdmin(admin.ModelAdmin):
    pass

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    pass
