from django import forms
from .models import Announcement, Category, Comment
from django.core.validators import ValidationError


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        exclude = ['views', 'create_announcement']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'category': forms.Select(attrs={
                'class': 'form-control',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control'
            }),

            'number': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'location': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),

            'image': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


    def clean_number(self):
        number = self.cleaned_data.get('number')
        cleaned = number.replace('+', '').replace('-', '').replace(' ', '')
        if not cleaned.isdigit():
            raise ValidationError(f"Faaqat raqam kiriting.")
        if len(number) == 9 or len(number) <= 15:
            raise ValidationError('Raqam kamida 9 xonali bo\'lsin')
        return number

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        if price <= 0:
            raise ValidationError("Narx 0 dan katta bo'lsin")

        name = cleaned_data.get('name')
        if len(name) <= 5:
            raise ValidationError('Kamida 5 belgidan iborat bo\'lsin')

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }