from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class NewsCommentsAbstractModel(models.Model):
    """ Abstract model for news and comments. """

    published_at = models.DateTimeField(
        auto_now_add=True,
    )
    text = models.TextField()

    class Meta:
        abstract = True
        ordering = ['-published_at']


class News(NewsCommentsAbstractModel):
    """ News model. """

    header = models.CharField(
        max_length=128,
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='author_news',
    )

    def __str__(self):
        return self.header


class Comment(NewsCommentsAbstractModel):
    """ Comment model. """

    news = models.ForeignKey(
        to=News,
        on_delete=models.CASCADE,
        related_name='news_comments',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='author_comments',
    )

    def __str__(self):
        return f'{self.author}|{self.published_at}'


class Like(models.Model):
    """ Like model. """

    news = models.ForeignKey(
        to=News,
        on_delete=models.CASCADE,
        related_name='news_likes',
    )
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_likes',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['news', 'author'],
                name='unique news and user'
            )
        ]

    def __str__(self):
        return f'{self.author}|{self.news.header}'
