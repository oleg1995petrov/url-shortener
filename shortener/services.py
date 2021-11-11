import re
import qrcode

from random import choice
from string import ascii_letters, digits
from io import BytesIO
from PIL import Image


SHORT_URL_SIZE = 5
AVAILABLE_CHARS = ascii_letters + digits
PATTERN = r'^(https?:\/\/)?(w{3}\.)?[-\wа-я]+\.[a-zа-я]{2,10}[-\w\.\/\?=&]*$'


def generate_random_code(chars=AVAILABLE_CHARS):
    """
    Generates random code as short_url for shortener object
    with SHORT_URL_SIZE length.
    """
    return ''.join([choice(chars) for _ in range(SHORT_URL_SIZE)])


def generate_short_url(model_instance):
    """
    Attaches the generated short_url to model_instance. 
    """
    random_code = generate_random_code()
    model = model_instance.__class__
    if model.objects.filter(short_url=random_code).exists():
        return generate_short_url(model_instance)
    return random_code


def check_long_url(long_url):
    """"
    Checks if long_url is valid.
    """
    is_correct = False
    if re.match(PATTERN, long_url):
        is_correct = True
    return is_correct


def clean_shortened_obj(shortened_obj):
    """
    Checks if long_url contents a protocol. If not, adds http:// to it.
    """
    long_url = shortened_obj.long_url
    if not long_url.startswith('http'):
        long_url = 'http://' + shortened_obj.long_url
    return long_url


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def make_qr_code(shortener_obj):
    qr = qrcode.make(shortener_obj.short_url)
    canvas = Image.new('RGB', (300, 300), 'white')
    canvas.paste(qr)
    fname = f'qr_code_{shortener_obj.short_url}.png'
    buffer = BytesIO()
    canvas.save(buffer, 'PNG')
    return (fname, buffer)
