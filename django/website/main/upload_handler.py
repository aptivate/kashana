import hashlib
import os.path
from django.conf import settings
from django.utils.deconstruct import deconstructible


@deconstructible
class UploadToHandler(object):
    path_base = ''
    unique_value_func = None

    def __init__(self, path_base, unique_value_func):
        self.path_base = path_base
        self.unique_value_func = unique_value_func

    def __call__(self, instance, filename):
        salt = settings.SECRET_KEY
        values = self.unique_value_func(instance)
        user_str = "".join(values)
        msg = hashlib.new('md5')  # Sucky hash, but good enough
        msg.update("{0}{1}".format(salt, user_str))
        new_path = os.path.join(self.path_base, msg.hexdigest()[:8], filename)
        return new_path
