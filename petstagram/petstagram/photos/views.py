from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import PhotoCreateForm, PhotoEditForm
from .models import Photo

UserModel = get_user_model()


@login_required
def photo_add(request):
    form = PhotoCreateForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        photo = form.save(commit=False)
        photo.user = request.user
        photo.save()
        form.save_m2m()
        return redirect('page-home')

    context = {
        'form': form,
    }
    return render(request, 'photos/photo-add-page.html', context)


def photo_details(request, pk):
    photo = Photo.objects.get(pk=pk)
    comments = photo.comment_set.all()
    user = request.user
    all_liked_photos_by_user = [like.like_to_photo_id for like in user.like_set.all()]

    context = {
        "photo": photo,
        'comments': comments,
        'is_owner': request.user == photo.user,
        'all_liked_photos_by_user': all_liked_photos_by_user
    }
    return render(request, 'photos/photo-details-page.html', context=context)


def photo_edit(request, pk):
    photo = Photo.objects.get(pk=pk)
    if request.method == 'GET':
        form = PhotoEditForm(instance=photo)
        context = {
            'form': form,
        }
        return render(request, 'photos/photo-edit-page.html', context)

    else:
        form = PhotoEditForm(request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return redirect('photo-details', pk)


def photo_delete(request, pk):
    photo = Photo.objects.get(pk=pk)
    photo.delete()
    return redirect('page-home')
