import re
import csv
from pathlib import Path

import pandas as pd

try:
    import pdfplumber
except Exception:
    pdfplumber = None

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'group_23_campus_support_resources'
CORPUS_PATH = DATA_DIR / '2_corpus_chunks.csv'
SOURCES_PATH = DATA_DIR / '1_sources.csv'
PDF_PATH = DATA_DIR / 'Handbook Undergraduate Studies 2025-26 150126.pdf'


def _normalize(text: str) -> str:
    return re.sub(r'\s+', ' ', text or '').strip()


def _split_to_chunks(text: str, min_words: int = 90, max_words: int = 150):
    text = _normalize(text)
    if not text:
        return []
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        end = min(i + max_words, len(words))
        if end < len(words) and (end - i) < min_words:
            end = min(i + min_words, len(words))
        window = words[i:end]
        chunks.append(' '.join(window))
        i = end
    return chunks


def _extract_pdf_chunks(limit: int = 120):
    if pdfplumber is None or not PDF_PATH.exists():
        return []
    all_text = []
    with pdfplumber.open(str(PDF_PATH)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ''
            if page_text.strip():
                all_text.append(page_text)
    raw = '\n\n'.join(all_text)
    paragraphs = [p.strip() for p in re.split(r'\n\s*\n', raw) if len(p.strip().split()) >= 30]
    chunks = []
    for para in paragraphs:
        chunks.extend(_split_to_chunks(para))
        if len(chunks) >= limit:
            break
    return chunks[:limit]


def _next_chunk_id(existing_ids):
    max_no = 0
    for cid in existing_ids:
        m = re.match(r'G23_C(\d+)', str(cid))
        if m:
            max_no = max(max_no, int(m.group(1)))
    return max_no + 1


def run():
    corpus = pd.read_csv(CORPUS_PATH)
    existing_text = set(corpus['text'].fillna('').str.strip().str.lower().tolist())
    next_id = _next_chunk_id(corpus['chunk_id'].tolist())

    additions = []

    pdf_chunks = _extract_pdf_chunks(limit=120)
    for chunk in pdf_chunks:
        key = chunk.strip().lower()
        if key in existing_text:
            continue
        additions.append({
            'group_id': 'G23',
            'chunk_id': f'G23_C{next_id:03d}',
            'topic': 'Handbook Expanded Data',
            'category': 'handbook_policies',
            'risk_level': 'L0_NORMAL',
            'title': f'UMT Handbook Extract {next_id:03d}',
            'text': chunk,
            'source_id': 'S001',
            'allowed_use': 'Campus policy and support information',
            'blocked_use': 'Legal or medical advice replacement',
            'language': 'English',
        })
        existing_text.add(key)
        next_id += 1

    if additions:
        corpus = pd.concat([corpus, pd.DataFrame(additions)], ignore_index=True)
        corpus.to_csv(CORPUS_PATH, index=False, quoting=csv.QUOTE_MINIMAL)

    print(f'Added {len(additions)} chunks. Total now: {len(corpus)}')


if __name__ == '__main__':
    run()
