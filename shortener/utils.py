from random import choice
from string import ascii_letters, digits

import re


SIZE = 5
AVAILABLE_CHARS = ascii_letters + digits
PATTERNS = (
    r'^(https?:\/\/)([\w\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?$',
    r'^([\w\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?$'
)


def generate_random_code(chars=AVAILABLE_CHARS):
    return ''.join([choice(chars) for _ in range(SIZE)])


def generate_url(model_instance):
    random_code = generate_random_code()
    model = model_instance.__class__

    if model.objects.filter(short_url=random_code).exists():
        return generate_url(model_instance)
    return random_code


def check_long_url(long_url):
    is_correct = False

    for pattern in PATTERNS:
        if re.match(pattern, long_url):
            is_correct = True
            break
    return is_correct


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip, x_forwarded_for
