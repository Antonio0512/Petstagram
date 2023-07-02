from django.contrib import admin

from petstagram.photos.models import Photo


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'date_published', 'description', 'get_tagged_pets')

    @staticmethod
    def get_tagged_pets(obj):
        return ", ".join([pet.pet_name for pet in obj.tagged_pets.all()])