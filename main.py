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


# Brute Force Simulator (Limited)

def brute_force_attack(target_hash, max_length=3):
    chars = string.ascii_lowercase
    start_time = time.time()
    attempts = 0

    for length in range(1, max_length + 1):
        for attempt in itertools.product(chars, repeat=length):
            attempts += 1
            guess = ''.join(attempt)
            if hash_password(guess) == target_hash:
                return guess, attempts, time.time() - start_time

    return None, attempts, time.time() - start_time


# Main Program

def main():
    print("🔐 Password Security Analysis Tool\n")

    password = input("Enter password to analyze: ")

    # Generate salt
    salt = generate_salt()
    hashed = hash_password(password)
    salted_hash = hash_password(password, salt)

    print("\n--- HASH RESULTS ---")
    print("SHA256 Hash:", hashed)
    print("Salt Used:", salt)
    print("Salted Hash:", salted_hash)

    # Entropy
    entropy = calculate_entropy(password)
    print("\n--- ENTROPY ANALYSIS ---")
    print(f"Password Entropy: {entropy} bits")

    # Dictionary Attack
    print("\n--- DICTIONARY ATTACK SIMULATION ---")
    result, attempts, duration = dictionary_attack(hashed)

    if result:
        print(f"Password cracked: {result}")
    else:
        print("Password not found in dictionary.")

    print(f"Attempts: {attempts}")
    print(f"Time taken: {round(duration, 4)} seconds")

    # Brute Force Attack (Limited)
    print("\n--- BRUTE FORCE SIMULATION (max length 3) ---")
    result, attempts, duration = brute_force_attack(hashed)

    if result:
        print(f"Password cracked: {result}")
    else:
        print("Password not cracked (within limit).")

    print(f"Attempts: {attempts}")
    print(f"Time taken: {round(duration, 4)} seconds")


if __name__ == "__main__":
    main()

