from flask import Flask, render_template, request
import hashlib
import bcrypt
import math
import string
import os
import json
import base64
from io import BytesIO
import matplotlib.pyplot as plt

app = Flask(__name__)


# Hashing Functions
def sha256_hash(password, salt=""):
    return hashlib.sha256((salt + password).encode()).hexdigest()

def bcrypt_hash(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


# Entropy Calculation
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
    if charset == 0:
        return 0
    return len(password) * math.log2(charset)


# Crack Time Estimator
def estimate_crack_time(entropy):
    guesses_per_second = 1_000_000_000  # 1B/sec
    total_guesses = 2 ** entropy
    seconds = total_guesses / guesses_per_second
    if seconds < 60:
        return f"{seconds:.2f} seconds"
    elif seconds < 3600:
        return f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        return f"{seconds/3600:.2f} hours"
    else:
        return f"{seconds/86400:.2f} days"


# GPU vs CPU Estimate
def gpu_attack_estimate(entropy):
    cpu_speed = 1_000_000_000
    gpu_speed = 100_000_000_000
    total_guesses = 2 ** entropy
    cpu_seconds = total_guesses / cpu_speed
    gpu_seconds = total_guesses / gpu_speed
    return {
        "cpu_time": cpu_seconds,
        "gpu_time": gpu_seconds
    }


# Dictionary Attack Simulation
def dictionary_attack_simulation(password, wordlist):
    target_hash = hashlib.sha256(password.encode()).hexdigest()
    attempts = 0
    for word in wordlist:
        attempts += 1
        word = word.strip()
        word_hash = hashlib.sha256(word.encode()).hexdigest()
        if word_hash == target_hash:
            return {"found": True, "password": word, "attempts": attempts}
    return {"found": False, "password": None, "attempts": attempts}


# Attempt Growth Graph
def generate_attempt_graph(password):
    charset = 94
    lengths = list(range(1, len(password)+2))
    attempts = [charset ** l for l in lengths]

    plt.figure()
    plt.plot(lengths, attempts, marker='o', color='cyan')
    plt.xlabel("Password Length")
    plt.ylabel("Number of Combinations (log scale)")
    plt.yscale("log")
    plt.title("Brute Force Attempt Growth")

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return graph_url


# Flask Route
@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        password = request.form["password"]
        file = request.files.get("wordlist")

        # Load uploaded wordlist or default
        wordlist = []
        if file:
            content = file.read().decode("utf-8")
            wordlist = content.splitlines()
        else:
            wordlist = ["123456", "password", "admin", "qwerty", "letmein"]

        # Hashes
        sha = sha256_hash(password)
        salted = sha256_hash(password, os.urandom(8).hex())
        bcrypt_hashed = bcrypt_hash(password)

        # Entropy & Crack Time
        entropy = calculate_entropy(password)
        crack_time = estimate_crack_time(entropy)

        # GPU Simulation
        gpu_result = gpu_attack_estimate(entropy)

        # Dictionary Attack Simulation
        attack_result = dictionary_attack_simulation(password, wordlist)

        # Growth Graph
        graph = generate_attempt_graph(password)

        # Result Dictionary
        result = {
            "sha": sha,
            "salted": salted,
            "bcrypt": bcrypt_hashed,
            "entropy": round(entropy,2),
            "crack_time": crack_time,
            "gpu_result": gpu_result,
            "attack_result": attack_result,
            "graph": graph
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)