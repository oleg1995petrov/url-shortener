from django.db import models

from .utils import generate_url
from django.utils import timezone


class Shortener(models.Model):
    """ """
    created = models.DateTimeField(auto_now_add=timezone.now)
    ip = models.CharField(max_length=15, default='')
    times_followed = models.PositiveIntegerField(default=0)
    long_url = models.CharField(max_length=1000, default='')
    short_url = models.CharField(max_length=5, unique=True, default='')

    class Meta:
        ordering = ['-created', '-id']

    def __str__(self, *args, **kwargs):
        return f'{self.long_url} --> {self.short_url}'

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = generate_url(self)

        super().save()
