import binascii
import hashlib


def invalid_text(text):
    if text == "":
        return True
    else:
        return False


def invalid_password(text):
    if text == "" or len(text) < 8:
        return True
    else:
        return False


def invalid_integer(text):
    if text == "":
        return True
    else:
        try:
            int(text)
            if int(text) == float(text):
                return False
            else:
                return True
        except:
            return True


def invalid_number(text):
    if text == "":
        return True
    else:
        try:
            float(text)
            return False
        except:
            return True

def hash_password(password):
    salt = "aoW~ihfa?JHCef£uqw2"
    iterations = 742
    crypt = hashlib.pbkdf2_hmac("sha256", bytearray(password, 'utf-8'), bytearray(salt, 'utf-8'), iterations)
    encrypted = str(binascii.hexlify(crypt))
    return encrypted
