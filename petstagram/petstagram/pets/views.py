from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from petstagram.accounts.models import PetstagramUser
from petstagram.common.forms import CommentForm
from petstagram.pets.models import Pet
from petstagram.pets.forms import PetForm, PetDeleteForm


@login_required
def pet_add(request):
    form = PetForm(request.POST or None)

    if form.is_valid():
        pet = form.save(commit=False)
        pet.user = request.user
        pet.save()
        return redirect('profile-page', pk=request.user.pk)

    context = {
        'form': form
    }

    return render(request, 'pets/pet-add-page.html', context)


def pet_details(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    owner = PetstagramUser.objects.get(username=username)
    all_photos = pet.photo_set.all()
    comment_form = CommentForm()

    context = {
        "pet": pet,
        'owner': owner,
        "all_photos": all_photos,
        "comment_form": comment_form
    }
    return render(request, 'pets/pet-details-page.html', context)


def pet_edit(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    owner = PetstagramUser.objects.get(username=username)
    if request.method == 'GET':
        form = PetForm(instance=pet)

        context = {
            'pet': pet,
            'owner': owner,
            'form': form,
        }
        return render(request, 'pets/pet-edit-page.html', context)

    else:
        form = PetForm(request.POST, instance=pet)
        if form.is_valid():
            form.save()
            return redirect('pet-details', username, pet_slug)


def pet_delete(request, username, pet_slug):
    pet = Pet.objects.get(slug=pet_slug)
    owner = PetstagramUser.objects.get(username=username)
    if request.method == 'POST':
        pet.delete()
        return redirect('profile-page', owner.pk)

    else:
        form = PetDeleteForm(instance=pet)
        context = {
            'form': form,
        }
        return render(request, 'pets/pet-delete-page.html', context)
