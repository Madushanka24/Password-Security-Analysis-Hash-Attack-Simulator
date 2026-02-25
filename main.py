from flask import Flask, render_template, request
import hashlib
import math
import json

app = Flask(__name__)

# Entropy calculator
def calculate_entropy(password):
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 10
    if any(not c.isalnum() for c in password):
        charset += 32

    if charset == 0:
        return 0

    return len(password) * math.log2(charset)


# Crack time estimator
def estimate_crack_time(entropy):
    guesses_per_second = 1_000_000_000 
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
    


#dictionary attack simulation   
def dictionary_attack_simulation(password, wordlist):
    target_hash = hashlib.sha256(password.encode()).hexdigest()

    attempts = 0

    for word in wordlist:
        attempts += 1
        word = word.strip()
        word_hash = hashlib.sha256(word.encode()).hexdigest()

        if word_hash == target_hash:
            return {
                "found": True,
                "password": word,
                "attempts": attempts
            }

    return {
        "found": False,
        "password": None,
        "attempts": attempts
    }


@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        password = request.form["password"]

        # SHA256 hash
        sha = hashlib.sha256(password.encode()).hexdigest()

        # Entropy
        entropy = calculate_entropy(password)

        # ADD IT HERE
        crack_time = estimate_crack_time(entropy)

        # Graph data (example)
        labels = list(range(1, 11))
        data = [2 ** i for i in labels]

        result = {
            "sha": sha,
            "entropy": round(entropy, 2),
            "crack_time": crack_time, 
            "labels": json.dumps(labels),
            "data": json.dumps(data)
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)