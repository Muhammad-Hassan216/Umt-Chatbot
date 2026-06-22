from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import os

app = Flask(__name__)

# ── Load Corpus ────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
CORPUS_PATH = os.path.join(BASE_DIR, 'group_23_campus_support_resources', '2_corpus_chunks.csv')

CORPUS_LOADED = False
df = None
vectorizer = None
tfidf_matrix = None

try:
    df = pd.read_csv(CORPUS_PATH)
    corpus_texts = (df['title'].fillna('') + ' ' + df['text'].fillna('')).tolist()
    vectorizer   = TfidfVectorizer(stop_words='english', ngram_range=(1, 2), max_features=5000)
    tfidf_matrix = vectorizer.fit_transform(corpus_texts)
    CORPUS_LOADED = True
    print(f"[OK] Corpus loaded: {len(df)} chunks")
except Exception as e:
    print(f"[WARN] Could not load corpus: {e}")

# ── Risk Classification ─────────────────────────────────────────────────────────
RISK_KEYWORDS = {
    'L3_CRISIS': [
        'suicide', 'suicidal', 'kill myself', 'kill my self', 'self-harm',
        'self harm', 'end my life', 'want to die', 'hurt myself', 'hurt my self',
        'take my life', 'not worth living', 'no reason to live', 'better off dead',
        'end it all', 'don\'t want to live'
    ],
    'L2_DISTRESS': [
        'hopeless', 'overwhelmed', "can't cope", 'cannot cope', 'falling apart',
        'breaking down', 'no point', 'worthless', 'i give up', 'giving up',
        'desperate', 'feel empty', 'feeling empty', 'nothing matters',
        'panic attack', 'devastated', 'can\'t go on', 'cannot go on'
    ],
    'L1_STRESS': [
        'stressed', 'anxious', 'anxiety', 'worried', 'nervous',
        "can't sleep", 'cannot sleep', 'struggling', 'pressure', 'exhausted',
        'burned out', 'depressed', 'depression', 'feeling down', 'upset',
        'frustrated', 'exam stress', 'exam anxiety', 'panic', 'overwhelmed'
    ]
}

def classify_risk(text: str) -> str:
    t = text.lower()
    for level in ['L3_CRISIS', 'L2_DISTRESS', 'L1_STRESS']:
        for kw in RISK_KEYWORDS[level]:
            if kw in t:
                return level
    return 'L0_NORMAL'

# ── Retrieval ───────────────────────────────────────────────────────────────────
def retrieve_chunks(query: str, top_k: int = 3):
    if not CORPUS_LOADED:
        return pd.DataFrame(), []
    qv     = vectorizer.transform([query])
    scores = cosine_similarity(qv, tfidf_matrix).flatten()
    top_i  = scores.argsort()[-top_k:][::-1]
    valid  = [(int(i), float(scores[i])) for i in top_i if scores[i] > 0.01]
    if not valid:
        return pd.DataFrame(), []
    indices, _ = zip(*valid)
    return df.iloc[list(indices)].copy(), list(indices)

# ── Response Templates ─────────────────────────────────────────────────────────
CRISIS_RESPONSE = (
    "🆘 **I'm concerned about your safety and want to make sure you get immediate help.**\n\n"
    "**Please contact emergency services right now:**\n\n"
    "- 🚨 **Police / Emergency: 15**\n"
    "- 🚑 **Rescue: 1122**\n\n"
    "**On Campus at UMT Sialkot:**\n\n"
    "- 🔒 **OSS&V (Safety Office):** Contact immediately on campus\n"
    "- 💙 **Happiness Center:** cc.center@umt.edu.pk\n\n"
    "**You matter. You are not alone. Help is available right now.**\n\n"
    "Please reach out to one of these contacts immediately. Your safety is the top priority."
)

FALLBACK = (
    "For any support needs at UMT Sialkot, please contact:\n\n"
    "- 💙 Happiness Center: **cc.center@umt.edu.pk**\n"
    "- 📞 City Campus: **+92 52 3241801-7**\n"
    "- 📧 General: **info@skt.umt.edu.pk**"
)

# Appended to every non-crisis response so users always verify with official source
SOURCE_DISCLAIMER = (
    "\n\n---\n"
    "📋 *Source: UMT Participants Handbook 2025-26 & Academic Calendar 2025-26. "
    "Contact info and policies may change — always verify at **[skt.umt.edu.pk](https://skt.umt.edu.pk)** "
    "or email **info@skt.umt.edu.pk** for the latest information.*"
)

def build_response(query: str, system: str):
    risk = classify_risk(query)

    # ── S0: Keyword-only, no RAG ────────────────────────────────────────────────
    if system == 'S0':
        q = query.lower()
        if any(w in q for w in ['counsel', 'mental', 'help', 'stress', 'anxiety', 'sad', 'depress', 'feel', 'emotion', 'happy', 'unhappy']):
            r = "UMT Sialkot has a **Happiness Center** with professional clinical psychologists. Email **cc.center@umt.edu.pk** to book a free, confidential appointment."
        elif any(w in q for w in ['library', 'book', 'study', 'research', 'tutor', 'lrc']):
            r = "The **Learning Resource Center** is open **8am–9pm** weekdays and **10am–5pm** Sundays. Visit for research support, book borrowing (4 books / 14 days), and databases."
        elif any(w in q for w in ['health', 'sick', 'doctor', 'medical', 'clinic', 'nurse', 'hospital']):
            r = "UMT has an **on-campus physician and nurse** providing free clinical evaluation and treatment. Visit the healthcare clinic — no additional cost to enrolled students."
        elif any(w in q for w in ['contact', 'phone', 'number', 'email', 'address', 'location', 'where', 'reach']):
            r = ("📍 **City Campus:** 21-A Small Industrial Estate, Shahabpura Road — Tel: **+92 52 3241801-7**\n\n"
                 "📍 **Iqbal Campus:** 2-KM Daska Road — Tel: **+92 52 3575234-36**\n\n"
                 "📧 **Email:** info@skt.umt.edu.pk")
        elif any(w in q for w in ['exam', 'final', 'test', 'midterm', 'result', 'grade']):
            r = "**Final Exams run June 29 – July 11, 2026.** For exam stress, the **Happiness Center** is available at cc.center@umt.edu.pk. The **Library** is open until 9pm for exam prep."
        elif any(w in q for w in ['tarbiyah', 'personal', 'growth', 'character', 'values', 'islamic']):
            r = "The **Tarbiyah Department** offers personal growth and values-based counseling through the **Ask Asiya desk** and Tarbiyah Ambassadors. Programs focus on character building and healthy relationships."
        else:
            r = "Thank you for reaching out. For support at UMT Sialkot, contact **info@skt.umt.edu.pk** or call **+92 52 3241801**. The **Happiness Center** provides free counseling at cc.center@umt.edu.pk."
        return r + SOURCE_DISCLAIMER, 'L0_NORMAL', []

    # ── S1 & S2: RAG ────────────────────────────────────────────────────────────
    chunks, _ = retrieve_chunks(query)

    if system == 'S1':
        # Plain RAG — no safety layer
        if len(chunks) == 0:
            return FALLBACK + SOURCE_DISCLAIMER, 'L0_NORMAL', []
        return chunks.iloc[0]['text'] + SOURCE_DISCLAIMER, 'L0_NORMAL', list(chunks['chunk_id'])

    # S2 — Safety-aware RAG
    if risk == 'L3_CRISIS':
        return CRISIS_RESPONSE, 'L3_CRISIS', []

    if len(chunks) == 0:
        return FALLBACK, risk, []

    best       = chunks.iloc[0]
    chunk_ids  = list(chunks['chunk_id'])

    prefix = suffix = ''
    if risk == 'L2_DISTRESS':
        prefix = ("💙 I hear you — what you're going through sounds really difficult, "
                  "and it takes courage to reach out. Support is here for you.\n\n")
        suffix = ("\n\n**Please connect with the Happiness Center at cc.center@umt.edu.pk "
                  "as soon as possible — they are trained professionals who genuinely care "
                  "and can help you through this.**")
    elif risk == 'L1_STRESS':
        prefix = "I understand you're feeling stressed — that's completely normal, especially around exam time. Here's what can help:\n\n"
        suffix = ("\n\nRemember, the **Happiness Center** (cc.center@umt.edu.pk) provides "
                  "free, confidential support anytime you need it. 💙")

    return prefix + best['text'] + suffix + SOURCE_DISCLAIMER, risk, chunk_ids

# ── Routes ─────────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid JSON'}), 400

    msg    = data.get('message', '').strip()
    system = data.get('system', 'S2')

    if not msg:
        return jsonify({'error': 'Empty message'}), 400
    if system not in ('S0', 'S1', 'S2'):
        system = 'S2'

    response, risk_level, chunk_ids = build_response(msg, system)

    return jsonify({
        'response':          response,
        'risk_level':        risk_level,
        'retrieved_chunks':  chunk_ids,
        'system':            system
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
