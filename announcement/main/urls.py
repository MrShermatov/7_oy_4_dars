from django.urls import path
from .views import (announcement_all, announcement_by_categories,
                    add_announcement, detail, update_announcement,
                    announcement_delete, add_category, update_category, delete_category,
                    create_comment, update_comment, delete_comment, add_announcementmark, navbar_announcementmark)

urlpatterns = [
    path('', announcement_all, name='home'),
    path('category/<int:category_id>/', announcement_by_categories, name='announcement_by_categories'),
    path('detail/<int:announcement_id>/', detail, name='detail'),
    path('add/', add_announcement, name='add_announcement'),
    path('update/<int:announcement_id>/', update_announcement, name='update_announcement'),
    path('delete/<int:announcement_id>/', announcement_delete, name='announcement_delete'),
    path('category/add/', add_category, name='add_category'),
    path('category/update/<int:category_id>/', update_category, name='update_category'),
    path('category/delete/<int:category_id>/', delete_category, name='delete_category'),

    path('announcement/add/comment/<int:announcement_id>/', create_comment,name='create_comment'),
    path('announcement/update/comment/<int:comment_id>/', update_comment,name='update_comment'),
    path('announcement/delete/comment/<int:comment_id>/<int:re_announcement_id>/', delete_comment,name='delete_comment'),

    path('announcement/add/announcementmark/<int:announcement_id>/', add_announcementmark,name='add_announcementmark'),
    path('wishlist/', navbar_announcementmark, name='navbar_announcementmark'),

]