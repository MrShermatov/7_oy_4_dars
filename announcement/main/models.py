from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name="Bo'lim nomi")

    class Meta:
        verbose_name = "Bo'lim"
        verbose_name_plural = "Bo'limlar"

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"PK: {self.pk}. Name: {self.name}"

class Author(models.Model):
    full_name = models.CharField(max_length=100, verbose_name="To'liq nomi")
    number = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name="Telefon raqam")
    address = models.CharField(max_length=100, null=True, blank=True, verbose_name='Adress')

    class Meta:
        verbose_name = "Elon beruvchi"
        verbose_name_plural = "Elon beruvchilar"

    def __str__(self):
        return self.full_name

class Announcement(models.Model):
    name = models.CharField(max_length=150, verbose_name="E'lon nomi")
    create_announcement = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Bo'limi")
    description = models.TextField(null=True, blank=True, verbose_name="Tavsif")
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True,verbose_name='Narxi')
    number = models.CharField(max_length=15, verbose_name='Telefon raqam')
    location = models.CharField(max_length=100, verbose_name="Manzil")
    views = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    author = models.ManyToManyField(Author, related_name='announcements', verbose_name='Elon egasi')
    image = models.ImageField(upload_to='images/', blank=True, null=True, verbose_name='Rasm')

    class Meta:
        verbose_name = "E'lon"
        verbose_name_plural = "E'lonlar"
        ordering = ('-create_announcement',)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"PK: {self.pk}. Name: {self.name}"

class AnnouncementStatus(models.Model):
    STATUS_ANNOUNCEMENT = [
        ('active', 'Faol'),
        ('noactive', 'Faol emas')
    ]
    status = models.CharField(max_length=30, choices=STATUS_ANNOUNCEMENT, default='active', verbose_name='Elon holati')
    announcement = models.OneToOneField('Announcement', on_delete=models.CASCADE, related_name='status')

    class Meta:
        verbose_name = "Holati"
        verbose_name_plural = "Holati"


class Comment(models.Model):
    text = models.CharField(max_length=500, verbose_name='Matn')
    created = models.DateTimeField(auto_now_add=True)
    re_announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    edited = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Fikr"
        verbose_name_plural = "Fikrlar"

    def __str__(self):
        return self.user.username if self.user else "Anonymous"

class AnnouncementMark(models.Model):
    re_announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='marks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Saralnganlar"

    def __str__(self):
        return f"{self.re_announcement.name} -> {self.user.username}"