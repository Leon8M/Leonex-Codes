from flask import Flask, render_template, request, jsonify
import json
from difflib import get_close_matches

app = Flask(__name__)

def see_brain(file_path: str) -> dict:
    with open(file_path, 'r') as f:
        data: dict = json.load(f)
    return data

def retain_brain(file_path: str, data: dict):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    

def find_best_match(user_query: str, questions: list[str]) -> str | None:
    matches: list = get_close_matches(user_query, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer(question: str, brain: dict) -> str | None:
    for q in brain["questions"]:
        if q["question"] == question:
            return q["answer"]

brain = see_brain('brain.json')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_input = request.json['user_input']
    best_match = find_best_match(user_input, [q["question"] for q in brain["questions"]])

    if best_match:
        answer = get_answer(best_match, brain)
    else:
        answer = "I don't know what you mean; please enlighten me"
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)
