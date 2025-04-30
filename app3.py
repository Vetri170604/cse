from flask import Flask, request, render_template
from transformers import pipeline
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import os
import sqlite3
from wordcloud import WordCloud
import speech_recognition as sr

app = Flask(__name__)
nltk.download('punkt')
nltk.download('stopwords')

sentiment_pipeline = pipeline("sentiment-analysis")
os.makedirs('static', exist_ok=True)

# Initialize DB
def init_db():
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS reviews (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    text TEXT,
                    sentiment TEXT,
                    score REAL,
                    complexity TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Emoji mapping
sentiment_emojis = {
    "POSITIVE": "😄",
    "NEGATIVE": "😞",
    "NEUTRAL": "😐"
}

# Neutral keywords
neutral_keywords = ["okay", "average", "neutral", "fine", "meh", "so-so"]

def is_neutral(text):
    return any(keyword in text.lower() for keyword in neutral_keywords)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload-audio', methods=['POST'])
def upload_audio():
    if 'audio_file' not in request.files:
        return "No audio file uploaded."

    file = request.files['audio_file']
    if file.filename == "":
        return "No file selected."

    wav_path = os.path.join("static", "uploaded.wav")
    file.save(wav_path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand the audio"
        except sr.RequestError:
            return "Speech Recognition API unavailable"

    return render_template('index.html', transcribed_text=text)

@app.route('/analyze', methods=['POST'])
def analyze():
    text = request.form.get('text', '').strip()
    if not text:
        return "No valid input provided."

    sentences = sent_tokenize(text)
    words = word_tokenize(text)

    results = {"POSITIVE": 0, "NEGATIVE": 0, "NEUTRAL": 0}
    detailed_results = []

    for sentence in sentences:
        result = sentiment_pipeline(sentence)[0]
        label = result['label']
        score = round(result['score'] * 100, 2)

        if score < 60 or is_neutral(sentence):
            label = "NEUTRAL"

        results[label] += 1
        detailed_results.append((sentence, label, score, sentiment_emojis[label]))

    overall = max(results, key=results.get)
    avg_score = round((results[overall] / len(sentences)) * 100, 2)

    # Word cloud
    wordcloud = WordCloud(width=400, height=200, background_color='white').generate(text)
    cloud_path = os.path.join('static', 'vetri.png')
    wordcloud.to_file(cloud_path)

    # Complexity
    word_count = len(words)
    sentence_count = len(sentences)
    avg_words = word_count / sentence_count
    if avg_words > 20:
        complexity = "High"
    elif avg_words > 10:
        complexity = "Moderate"
    else:
        complexity = "Low"

    # Save to DB
    conn = sqlite3.connect('reviews.db')
    c = conn.cursor()
    c.execute('''INSERT INTO reviews (text, sentiment, score, complexity)
                 VALUES (?, ?, ?, ?)''', (text, overall, avg_score, complexity))
    conn.commit()
    conn.close()

    # Suggestion
    if overall == "NEGATIVE":
        suggestion = "Try improving areas mentioned in the negative feedback."
        recommendation = "Do Not Buy"
    elif overall == "POSITIVE":
        suggestion = "Customers are happy. Keep it up!"
        recommendation = "Buy"
    else:
        suggestion = "Neutral feedback detected. Encourage more detailed reviews."
        recommendation = "Evaluate further"

    return render_template(
        'result.html',
        text=text,
        sentiment=overall,
        score=avg_score,
        sentence_results=detailed_results,
        chart_url='vetri.png',
        complexity=complexity,
        suggestion=suggestion,
        recommendation=recommendation
    )

if __name__ == '__main__':
    app.run(debug=True)
