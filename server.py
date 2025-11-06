from flask import Flask, render_template_string, request
import csv
from datetime import datetime

app = Flask(__name__)

questions = [
"I know when to speak about my personal problems to others",
"When I am faced with obstacles, I remember times I faced similar obstacles and overcame them",
"I expect that I will do well on most things I try",
"Other people find it easy to confide in me",
"I find it hard to understand the non-verbal messages of other people",  # reverse
"Some of the major events of my life have led me to re-evaluate what is important and not important",
"When my mood changes, I see new possibilities",
"Emotions are one of the things that make my life worth living",
"I am aware of my emotions as I experience them",
"I expect good things to happen",
"I like to share my emotions with others",
"When I experience a positive emotion, I know how to make it last",
"I arrange events others enjoy",
"I seek out activities that make me happy",
"I am aware of the non-verbal messages I send to others",
"I present myself in a way that makes a good impression on others",
"When I am in a positive mood, solving problems is easy for me",
"By looking at their facial expressions, I recognize the emotions people are experiencing",
"I know why my emotions change",
"When I am in a positive mood, I am able to come up with new ideas",
"I have control over my emotions",
"I easily recognize my emotions as I experience them",
"I motivate myself by imagining a good outcome to tasks I take on",
"I compliment others when they have done something well",
"I am aware of the non-verbal messages other people send",
"When another person tells me about an important event in his or her life, I almost feel as though I have experienced this event myself",
"When I feel a change in emotions, I tend to come up with new ideas",
"When I am faced with a challenge, I give up because I believe I will fail",  # reverse
"I know what other people are feeling just by looking at them",
"I help other people feel better when they are down",
"I use good moods to help myself keep trying in the face of obstacles",
"I can tell how people are feeling by listening to the tone of their voice",
"It is difficult for me to understand why people feel the way they do"  # reverse
]

reverse_indices = [4, 27, 32]  # 0-based indices
CSV_FILE = "emotional_intelligence_data.csv"

# HTML Templates
INDEX_TEMPLATE = open("index.html").read()

RESULT_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>EI Test Result</title>
<style>
  body { font-family: Arial, sans-serif; max-width: 700px; margin: auto; padding: 20px; line-height: 1.6; }
  h1 { color: #0056b3; text-align: center; }
  .result { background: #f0f7ff; border: 1px solid #b3d7ff; border-radius: 8px; padding: 20px; }
</style>
</head>
<body>
  <h1>Your Emotional Intelligence Score</h1>
  <div class="result">
    <h2>Total Score: {{ score }}</h2>
    <p>{{ interpretation }}</p>
    <hr>
    <p><em>Your response has been recorded (Age: {{ age }}, Gender: {{ gender }}).</em></p>
  </div>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(INDEX_TEMPLATE, questions=list(enumerate(questions)))

@app.route("/submit", methods=["POST"])
def submit():
    age = request.form.get("age")
    gender = request.form.get("gender")

    # Calculate score
    total_score = 0
    for i in range(len(questions)):
        val = int(request.form.get(f"q{i}", 0))
        if i in reverse_indices:
            val = 6 - val
        total_score += val

    # Save to CSV
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().isoformat(), age, gender, total_score])

    # Interpretation
    if total_score < 111:
        interp = "You may face challenges identifying or managing emotions, but EI can grow with awareness and practice."
    elif total_score <= 137:
        interp = "You have balanced emotional awareness and empathy. You manage emotions fairly well."
    else:
        interp = "You have strong emotional intelligence and resilience."

    return render_template_string(RESULT_TEMPLATE,
                                  score=total_score,
                                  interpretation=interp,
                                  age=age, gender=gender)

if __name__ == "__main__":
    app.run(debug=True)
