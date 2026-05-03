from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from .models import Category, Announcement, Comment, AnnouncementMark
from .forms import CategoryForm, AnnouncementForm, CommentForm
from django.http import HttpRequest


def announcement_all(request: HttpRequest):
    categories = Category.objects.all()

    if request.user.is_authenticated:
        mark_list = AnnouncementMark.objects.filter(user=request.user).values_list('re_announcement_id', flat=True)

        if request.GET.get('ad_marks'):
            announcement = Announcement.objects.filter(id__in=mark_list)
        else:
            announcement = Announcement.objects.all()

        for item in announcement:
            if item.pk in mark_list:
                item.like = True
    else:
        announcement = Announcement.objects.all()
        mark_list = []
    paginator = Paginator(announcement, per_page=3)
    page = paginator.page(request.GET.get('page', 1))
    context = {
        'categories': categories,
        'page': page,
        'mark_list': mark_list,
        'title': "EloHub"
    }
    return render(request, 'main/index.html', context)

def detail(request: HttpRequest, announcement_id):
    categories = Category.objects.all()
    announcement = get_object_or_404(Announcement, id=announcement_id)

    context = {
        'categories': categories,
        'announcement': announcement
    }

    return render(request, 'main/detail.html', context)


def announcement_by_categories(request: HttpRequest, category_id):
    categories = Category.objects.all()
    announcement = Announcement.objects.filter(category_id=category_id)
    category = get_object_or_404(Category, id=category_id)

    context = {
        'categories': categories,
        'announcement': announcement,
        'category': category

    }

    return render(request, 'main/index.html', context)


def add_announcement(request: HttpRequest):
    if request.user.is_staff:
        if request.method == 'POST':
            form = AnnouncementForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                announcement = form.save()
                messages.success(request, "Elon muvaffaqiyatli qo'shildi !!!")
                return redirect('detail', announcement_id=announcement.id)
        else:
            form = AnnouncementForm()

        context = {
            'form': form
        }
        return render(request, 'main/add_announcement.html', context)
    else:
        return redirect('home')


def update_announcement(request: HttpRequest, announcement_id: int):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    if request.user.is_staff:
        if request.method == 'POST':
            form = AnnouncementForm(data=request.POST, files=request.FILES, instance=announcement)
            if form.is_valid():
                form.save()
                return redirect('detail', announcement_id=announcement.id)
        else:
            form = AnnouncementForm(instance=announcement)

        context = {
            'form': form
        }
        return render(request, 'main/add_announcement.html', context)
    else:
        return redirect('home')


def announcement_delete(request: HttpRequest, announcement_id: int):
    announcement = get_object_or_404(Announcement, id=announcement_id)
    if request.user.is_staff:
        if request.method == 'POST':
            announcement.delete()
            messages.success(request,'Kitop muvaffaqilyatli ochirildi')
            return redirect('home')

        context = {
            'announcement': announcement
        }
        messages.error(request, 'shu kitopni ochirmoqchimisz')
        return render(request, 'main/delete_announcement.html', context)
    else:
        return redirect('home')


def add_category(request: HttpRequest):
    if request.user.is_staff:
        if request.method == 'POST':
            form = CategoryForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = CategoryForm()

        context = {'form': form}
        return render(request, 'main/add_category.html', context)
    else:
        return redirect('home')


def update_category(request: HttpRequest, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    if request.user.is_staff:
        if request.method == 'POST':
            form = CategoryForm(data=request.POST, files=request.FILES, instance=category)
            if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form = CategoryForm(instance=category)

        context = {'form': form}
        return render(request, 'main/add_category.html', context)
    else:
        return redirect('home')


def delete_category(request: HttpRequest, category_id: int):
    category = get_object_or_404(Category, id=category_id)
    if request.user.is_staff:
        if request.method == 'POST':
            category.delete()
            return redirect('home')

        context = {'category': category}
        return render(request, 'main/delete_category.html', context)
    else:
        return redirect('home')


# ------------------------------start comment---------------------------
def create_comment(request: HttpRequest, announcement_id: int):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CommentForm(data=request.POST)
            if form.is_valid():
                announcement = get_object_or_404(Announcement, pk=announcement_id)
                comment = form.save(commit=False)
                comment.re_announcement = announcement
                comment.user = request.user
                comment.save()
        return redirect('detail', announcement_id=announcement_id)
    else:
        return redirect('home')


@login_required(login_url='home')
def update_comment(request: HttpRequest, comment_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user:
        if request.method == 'POST':
            form = CommentForm(data=request.POST, instance=comment)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.edited = True
                comment.save()
                return redirect('detail', announcement_id=comment.re_announcement.id)
        else:
            form = CommentForm(instance=comment)

        return render(request, 'main/update_comment.html', {'form': form, 'comment': comment})
    return redirect('detail', announcement_id=comment.re_announcement.id)


@login_required(login_url='home')
def delete_comment(request: HttpRequest, comment_id: int, re_announcement_id: int):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user == comment.user or request.user.is_superuser:
        comment.delete()
    return redirect('detail', announcement_id=re_announcement_id)


# ------------------------------end comment-----------------------------

# ------------------------------Start AnnouncementMark-----------------------------
@login_required(login_url='home')
def add_announcementmark(request: HttpRequest, announcement_id: int):
    announcement = get_object_or_404(Announcement, pk=announcement_id)
    announcementmark, created = AnnouncementMark.objects.get_or_create(re_announcement=announcement, user=request.user)
    if not created:
        announcementmark.delete()

    next_url = request.META.get('HTTP_REFERER', 'home')
    return redirect(next_url)


@login_required(login_url='home')
def navbar_announcementmark(request: HttpRequest):
    announcements = Announcement.objects.filter(marks__user=request.user)
    mark_list = announcements.values_list('id', flat=True)

    categories = Category.objects.all()
    context = {
        'announcement': announcements,
        'mark_list': mark_list,
        'categories': categories,
    }

    return render(request, 'main/index.html', context)
# ------------------------------end AnnouncementMark-----------------------------
