import os.path
from PIL import Image
from django.conf import settings
    

AUTO_GENERATE_AVATAR_SIZES = getattr(settings, 'AUTO_GENERATE_AVATAR_SIZES', (80,40))
AVATAR_RESIZE_METHOD = getattr(settings, 'AVATAR_RESIZE_METHOD', Image.ANTIALIAS)
AVATAR_STORAGE_DIR = getattr(settings, 'AVATAR_STORAGE_DIR', 'avatars')
AVATAR_GRAVATAR_BACKUP = getattr(settings, 'AVATAR_GRAVATAR_BACKUP', True)
AVATAR_DEFAULT_URL = getattr(settings, 'AVATAR_DEFAULT_URL', 
    settings.STATIC_URL +  'images/org_photo_default.jpg')

# from django.db.models import signals
# from evesch.org.avatar.models import Avatar


# def create_default_thumbnails(instance=None, created=False, **kwargs):
#     if created:
#         for size in AUTO_GENERATE_AVATAR_SIZES:
#             instance.create_thumbnail(size)
# signals.post_save.connect(create_default_thumbnails, sender=Avatar)