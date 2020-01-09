import base64
import fileinput
import string
import sys

from django.conf import settings


class Encryption:
    def __init__(self):
        return

    def encrypt_password(self, encode_data):
        local_settings_path = settings.PROJECT_ROOT + '/local_settings.py'
        newline = 'ENCODE_DATA = "' + base64.b64encode(encode_data) + '"'
        lnum = 1
        for line in fileinput.FileInput(local_settings_path, inplace=1):
            if lnum == 2:
                result = newline + "\n"
            else:
                result = line
            lnum = lnum + 1
            sys.stdout.write(result)
