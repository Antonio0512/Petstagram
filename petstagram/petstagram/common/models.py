from django.db import models
from petstagram.accounts.models import PetstagramUser
from petstagram.photos.models import Photo


class Comment(models.Model):
    text = models.TextField(
        max_length=300
    )
    date_time_of_publication = models.DateTimeField(
        auto_now_add=True
    )
    comment_to_photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE
    )
    user_that_commented = models.ForeignKey(
        PetstagramUser,
        on_delete=models.RESTRICT
    )


class Like(models.Model):
    like_to_photo = models.ForeignKey(
        Photo,
        on_delete=models.CASCADE
    )
    user_that_liked = models.ForeignKey(
        PetstagramUser,
        on_delete=models.RESTRICT
    )
