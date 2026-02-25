import hashlib
import time
import math
import itertools
import string
import random

# Hashing Functions

def hash_password(password, salt=""):
    return hashlib.sha256((salt + password).encode()).hexdigest()

def generate_salt(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
