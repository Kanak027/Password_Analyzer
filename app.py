from flask import Flask, render_template, request, jsonify
import re
import openai
from pyzxcvbn import zxcvbn

app = Flask(__name__)

# Load RockYou passwords into memory
def load_rockyou():
    try:
        with open("rockyou.txt", "r", encoding="latin-1") as file:
            return set(file.read().splitlines())
    except FileNotFoundError:
        print("Error: rockyou.txt not found.")
        return set()

leaked_passwords = load_rockyou()

def check_password_strength(password):
    """Evaluate password strength based on length and diversity."""
    length_score = min(len(password) / 12, 1) * 50
    digit_score = 10 if re.search(r"\d", password) else 0
    uppercase_score = 10 if re.search(r"[A-Z]", password) else 0
    lowercase_score = 10 if re.search(r"[a-z]", password) else 0
    special_char_score = 20 if re.search(r"[@$!%*?&]", password) else 0

    total_score = length_score + digit_score + uppercase_score + lowercase_score + special_char_score
    return round(min(total_score, 100), 2)

def estimate_time_to_crack(password):
    """Estimate time to crack the password."""
    result = zxcvbn(password)
    return result["crack_times_display"]["offline_fast_hashing_1e10_per_second"]

def is_password_leaked(password):
    """Check if the password is in the leaked RockYou dataset."""
    return password in leaked_passwords

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze_password():
    """Analyze password strength, check if leaked, and suggest improvements."""
    data = request.get_json()
    password = data.get("password", "")

    strength = check_password_strength(password)
    time_to_crack = estimate_time_to_crack(password)
    leaked = is_password_leaked(password)
    
    return jsonify({
        "password": password,
        "strength": f"{strength}%",
        "time_to_crack": time_to_crack,
        "leaked": leaked
    })

if __name__ == '__main__':
    app.run(debug=True)
