from django.db import models

from vgo.apps.core.models import TimestampedModel


class Post(TimestampedModel):
    slug = models.SlugField(db_index=True, max_length=255, unique=True)
    title = models.CharField(db_index=True, max_length=255)

    description = models.TextField()
    body = models.TextField()

    # Every post must have an author. This will answer questions like "Who
    # gets credit for writing this post?" and "Who can edit this post?".
    # Unlike the `User` <-> `Profile` relationship, this is a simple foreign
    # key (or one-to-many) relationship. In this case, one `Profile` can have
    # many `Post`s.
    author = models.ForeignKey(
        'authentication.User', on_delete=models.CASCADE, related_name='posts'
    )

    def __str__(self):
        return self.title

class Comment(TimestampedModel):
    body = models.TextField()

    post = models.ForeignKey(
        'post.Post', related_name='comments', on_delete=models.CASCADE
    )

    author = models.ForeignKey(
        'authentication.User', related_name='comments', on_delete=models.CASCADE
    )
