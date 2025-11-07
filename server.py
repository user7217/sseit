from flask import Flask, render_template, request
import csv, os
from datetime import datetime

app = Flask(__name__)

# =============================
# --- 1. Schutte EI Test ---
# =============================
sseit_questions = [
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
sseit_reverse = [4, 27, 32]
SSEIT_CSV = "sseit_responses.csv"

# =============================
# --- 2. EMSA Test ---
# =============================
emsa_questions = [
    "I often get mentally restless over small issues.",
    "I feel anxious when I think about upcoming events.",
    "I lose focus and leave things unfinished.",
    "I often rely on others to get my personal work done.",
    "My desires often conflict with my real goals.",
    "I get irritated or angry easily.",
    "I can be inflexible about my opinions or habits.",
    "I sometimes feel jealous of people who succeed.",
    "I find it hard to calm down when angry.",
    "I get lost in daydreams and imagination.",
    "Failure makes me feel inferior or less capable.",
    "I frequently feel uneasy or dissatisfied without clear reason.",
    "I sometimes mock or tease others unnecessarily.",
    "I tend to blame others when things go wrong.",
    "I start arguments when my ideas aren’t accepted.",
    "I often feel mentally exhausted or drained.",
    "I behave more aggressively than my friends.",
    "I often drift into fantasies instead of focusing on reality.",
    "I tend to put my own needs above everyone else’s.",
    "I am rarely content with myself.",
    "I struggle to maintain good relations with friends or coworkers.",
    "I sometimes hold grudges or dislike others easily.",
    "I find it difficult to appreciate or compliment others.",
    "I avoid social gatherings or group activities.",
    "I spend much of my time thinking only about myself.",
    "I occasionally tell lies to avoid problems.",
    "I sometimes exaggerate or bluff to impress others.",
    "I prefer to be alone rather than with people.",
    "I take pride in my abilities and achievements.",
    "I often try to escape from work I dislike.",
    "I hide my skills even when I know I can do something.",
    "I act like I know things even when I don’t.",
    "When I make mistakes, I try to prove myself right instead of admitting them.",
    "I often experience unexplained fears.",
    "I lose emotional balance under pressure.",
    "I sometimes take things that aren’t mine or act unethically.",
    "I ignore moral limits when it suits me.",
    "I often have a pessimistic view of life.",
    "I find it difficult to stick to my decisions.",
    "I am intolerant of opinions that differ from mine.",
    "People often find me unreliable.",
    "I frequently clash with others’ opinions.",
    "I prefer following others instead of taking initiative.",
    "I often reject group opinions to assert myself.",
    "Others sometimes see me as careless or irresponsible.",
    "I show little interest in other people’s tasks.",
    "People hesitate to seek my help.",
    "I put my priorities above those of everyone else."
]
EMSA_CSV = "emsa_responses.csv"

# Create CSVs if missing
for csv_file, headers in [
    (SSEIT_CSV, ["Timestamp", "Age", "Gender", "Score", "Category"]),
    (EMSA_CSV, ["Timestamp", "Age", "Gender", "Score", "Category"]),
]:
    if not os.path.exists(csv_file):
        with open(csv_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)

# =============================
# --- ROUTES ---
# =============================

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/sseit")
def sseit():
    return render_template("sseit.html", questions=list(enumerate(sseit_questions)))

@app.route("/emsa")
def emsa():
    return render_template("emsa.html", questions=list(enumerate(emsa_questions)))

@app.route("/submit_sseit", methods=["POST"])
def submit_sseit():
    age = request.form.get("age")
    gender = request.form.get("gender")
    score = 0
    for i in range(len(sseit_questions)):
        val = int(request.form.get(f"q{i}", 0))
        if i in sseit_reverse:
            val = 6 - val
        score += val
    if score < 111:
        cat = "Low EI"
    elif score <= 137:
        cat = "Moderate EI"
    else:
        cat = "High EI"
    with open(SSEIT_CSV, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.now().isoformat(), age, gender, score, cat])
    return render_template("result.html", title="SSEIT Result", score=score, category=cat, age=age, gender=gender)

@app.route("/submit_emsa", methods=["POST"])
def submit_emsa():
    age = request.form.get("age")
    gender = request.form.get("gender")
    score = sum(int(request.form.get(f"q{i}", 0)) for i in range(len(emsa_questions)))
    if score <= 80:
        cat = "Extremely Stable (Highly Mature)"
    elif score <= 88:
        cat = "Moderately Stable"
    elif score <= 106:
        cat = "Unstable"
    elif score <= 139:
        cat = "Moderately Unstable"
    else:
        cat = "Extremely Unstable (Emotionally Immature)"
    with open(EMSA_CSV, "a", newline="", encoding="utf-8") as f:
        csv.writer(f).writerow([datetime.now().isoformat(), age, gender, score, cat])
    return render_template("result.html", title="EMSA Result", score=score, category=cat, age=age, gender=gender)

if __name__ == "__main__":
    app.run(debug=True)
