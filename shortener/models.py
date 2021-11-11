import qrcode

from django.core.files import File
from django.db import models
from django.utils import timezone

from shortener import services
from users.models import User


class ShortenerBase(models.Model):
    """
    Abstract shortener model.
    """
    class Meta:
        abstract = True
        ordering = ['-id']
    
    long_url = models.CharField(max_length=255, default='')
    short_url = models.CharField(max_length=100, unique=True,
                                 default='')

    def __str__(self, *args, **kwargs):
        return f'{self.long_url} --> {self.short_url}'

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = services.generate_short_url(self)
        super().save(*args, **kwargs)


class AnonymousShortener(ShortenerBase):
    """
    Shortener model for anonymous users.
    """
    ip = models.CharField(max_length=15, default='')


class Shortener(ShortenerBase):
    """
    Shortener model for authenticated users.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                             related_name='links')
    created_at = models.DateTimeField(auto_now_add=timezone.now)
    times_followed = models.PositiveIntegerField(default=0)
    hidden = models.BooleanField(default=False)
    qr_code = models.ImageField(upload_to='qr_codes', null=True,
                                blank=True)

    def save(self, *args, **kwargs):
        if not self.short_url:
            self.short_url = services.generate_short_url(self)
            fname, buffer = services.make_qr_code(self)
            self.qr_code.save(fname, File(buffer), save=False)
        super().save(*args, **kwargs)
