from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"PK: {self.pk}. Name: {self.name}"

class Announcement(models.Model):
    name = models.CharField(max_length=150)
    create_announcement = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    number = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"PK: {self.pk}. Name: {self.name}"

class Comment(models.Model):
    text = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    re_announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    edited = models.BooleanField(default=False)
    def __str__(self):
        return self.user.username if self.user else "Anonymous"

class AnnouncementMark(models.Model):
    re_announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='marks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.re_announcement.name} -> {self.user.username}"