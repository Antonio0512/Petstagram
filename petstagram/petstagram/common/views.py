from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, resolve_url
from pyperclip import copy

from petstagram.common.forms import CommentForm, SearchForm
from .models import Like
from ..photos.models import Photo


@login_required
def home(request):
    all_photos = Photo.objects.all()
    comment_form = CommentForm()
    search_form = SearchForm()
    user = request.user
    all_liked_photos_by_user = [like.like_to_photo_id for like in user.like_set.all()]

    if request.method == 'POST':
        search_form = SearchForm(request.POST)
        if search_form.is_valid():
            all_photos = all_photos.filter(
                tagged_pets__pet_name__icontains=search_form.cleaned_data['pet_name']
            )

    context = {
        "all_photos": all_photos,
        "comment_form": comment_form,
        "search_form": search_form,
        'all_liked_photos_by_user': all_liked_photos_by_user
    }

    return render(request, 'common/home-page.html', context=context)


@login_required
def like_functionality(request, photo_id):
    photo = Photo.objects.get(id=photo_id)
    user_liked_photos = Like.objects.filter(
        like_to_photo_id=photo_id,
        user_that_liked=request.user)

    if user_liked_photos:
        user_liked_photos.delete()
    else:
        like = Like(like_to_photo=photo, user_that_liked=request.user)
        like.save()

    return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')


def copy_link_to_clipboard(request, photo_id):
    copy(request.META['HTTP_HOST'] + resolve_url('photo-details', photo_id))

    return redirect(request.META['HTTP_REFERER'] + f"#{photo_id}")


def add_comment(request, photo_id):
    if request.method == 'POST':
        photo = Photo.objects.get(id=photo_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comment_to_photo = photo
            comment.user_that_commented = request.user
            comment.save()

        return redirect(request.META['HTTP_REFERER'] + f'#{photo_id}')
