from django.contrib import admin

from shortener.models import AnonymousShortener, Shortener


admin.site.register(AnonymousShortener)
admin.site.register(Shortener)
