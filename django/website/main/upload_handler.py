import hashlib
import os.path
from django.conf import settings


def create_upload_to_handler(path_base, unique_value_func):
    '''
    Return handler for creating reasonably collision-free file names.

    Does not need to be very secretive, but should prevent upload conflicts
    and very basic guessing while being as readable as possible.

    QUESTION: Should the same file uploaded by the same user result in the
        same file name? (currently it does)
    '''
    def get_file_path(instance, filename):
        salt = settings.SECRET_KEY
        values = unique_value_func(instance)
        user_str = "".join(values)
        msg = hashlib.new('md5')  # Sucky hash, but good enough
        msg.update("{0}{1}".format(salt, user_str))
        new_path = os.path.join(path_base, msg.hexdigest()[:8], filename)
        return new_path
    return get_file_path
