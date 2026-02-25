from flask import Flask, render_template, request
import hashlib
import bcrypt
import math
import string
import matplotlib.pyplot as plt
import os
import base64
from io import BytesIO

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

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)



# Attempt Growth Graph


def generate_attempt_graph(password):
    charset = 94  # full ASCII set assumption
    lengths = list(range(1, len(password) + 2))
    attempts = [charset ** l for l in lengths]

    plt.figure()
    plt.plot(lengths, attempts)
    plt.xlabel("Password Length")
    plt.ylabel("Number of Combinations")
    plt.title("Brute Force Growth (Exponential)")
    plt.yscale("log")

    img = BytesIO()
    plt.savefig(img, format="png")
    img.seek(0)
    graph_url = base64.b64encode(img.getvalue()).decode()
    plt.close()

    return graph_url



# Routes

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        password = request.form["password"]

        salt = os.urandom(8).hex()

        sha_hash = sha256_hash(password)
        salted_hash = sha256_hash(password, salt)
        bcrypt_hashed = bcrypt_hash(password)

        entropy = calculate_entropy(password)
        graph = generate_attempt_graph(password)

        return render_template(
            "index.html",
            password=password,
            sha_hash=sha_hash,
            salted_hash=salted_hash,
            bcrypt_hash=bcrypt_hashed,
            entropy=entropy,
            graph=graph
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)