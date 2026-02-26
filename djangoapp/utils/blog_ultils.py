import string
from random import SystemRandom
from django.utils.text import slugify

def random_latters(k=5):
    
    return ''.join(SystemRandom().choices(
        string.ascii_letters + string.digits,
        k=k
    ))
    
def new_slugfy(text, k=5):
    return slugify(text) + '-' + random_latters(k)