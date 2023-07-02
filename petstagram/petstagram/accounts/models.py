from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models


class PetstagramUser(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2, 'Name should have at least 2 characters!'),
                    RegexValidator(r'^[A-Za-z]+$',
                                   "Ensure this value contains only letters!")])

    last_name = models.CharField(
        max_length=30,
        validators=[MinLengthValidator(2, 'Name should have at least 2 characters!'),
                    RegexValidator(r'^[A-Za-z]+$',
                                   "Ensure this value contains only letters!")])

    profile_picture = models.URLField()

    gender = models.CharField(
        max_length=30,
        choices=(
            ('Male', 'Male'),
            ('Female', 'Female'),
            ('Do not show', 'Do not show')
        )
    )

