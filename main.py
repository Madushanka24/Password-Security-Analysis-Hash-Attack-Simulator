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


# Entropy Calculator

def calculate_entropy(password):
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(c in string.punctuation for c in password):
        charset += 32

    entropy = len(password) * math.log2(charset) if charset else 0
    return round(entropy, 2)



# Dictionary Attack Simulator

def dictionary_attack(target_hash, wordlist_file="wordlist.txt"):
    start_time = time.time()
    attempts = 0

    try:
        with open(wordlist_file, "r") as file:
            for word in file:
                word = word.strip()
                attempts += 1
                if hash_password(word) == target_hash:
                    return word, attempts, time.time() - start_time
    except FileNotFoundError:
        return None, 0, 0

    return None, attempts, time.time() - start_time

