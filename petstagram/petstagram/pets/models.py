from django.db import models
from django.utils.text import slugify
from ..accounts.models import PetstagramUser


class Pet(models.Model):
    pet_name = models.CharField(max_length=30)
    pet_photo = models.URLField()
    pet_birth = models.DateField(blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    user = models.ForeignKey(PetstagramUser, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if not self.slug:
            self.slug = slugify(f'{self.id}-{self.pet_name}')

        return super().save(*args, **kwargs)

    def __str__(self):
        return self.pet_name
