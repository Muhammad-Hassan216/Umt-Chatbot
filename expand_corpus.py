import re
import csv
from pathlib import Path

import pandas as pd

try:
    import pdfplumber
except Exception:
    pdfplumber = None

try:
    import requests
    from bs4 import BeautifulSoup
except Exception:
    requests = None
    BeautifulSoup = None


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'group_23_campus_support_resources'
CORPUS_PATH = DATA_DIR / '2_corpus_chunks.csv'
SOURCES_PATH = DATA_DIR / '1_sources.csv'
PDF_PATH = DATA_DIR / 'Handbook Undergraduate Studies 2025-26 150126.pdf'
SCRAPE_TIMEOUT_SECONDS = 15


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


def _scrape_chunks():
    if requests is None or BeautifulSoup is None:
        return []
    urls = [
        'https://skt.umt.edu.pk/Contact-Us.aspx',
        'https://skt.umt.edu.pk/Admissions.aspx',
        'https://skt.umt.edu.pk/News-Events.aspx',
    ]
    scraped = []
    for url in urls:
        try:
            res = requests.get(url, timeout=SCRAPE_TIMEOUT_SECONDS)
            if res.status_code != 200:
                continue
            soup = BeautifulSoup(res.text, 'html.parser')
            title = _normalize(soup.title.get_text()) if soup.title else 'UMT Sialkot Web Page'
            blocks = [el.get_text(' ', strip=True) for el in soup.select('p, li')]
            text = _normalize(' '.join(blocks[:120]))
            for chunk in _split_to_chunks(text, min_words=70, max_words=130)[:2]:
                scraped.append((title, chunk))
        except Exception:
            continue
    return scraped


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

    manual_chunks = [
        (
            'Financial Aid and Fee Support',
            'UMT provides financial support pathways that may include scholarships merit support and fee concessions depending on eligibility and institutional policy. Students facing payment challenges should contact the admissions or student affairs office early and share relevant documents before fee deadlines. Official departments can guide students on current criteria timelines and required forms. If you are unsure where to begin use info@skt.umt.edu.pk and ask to be routed to financial aid support for your campus.',
            'financial_support'
        ),
        (
            'Hostel and Accommodation Guidance',
            'Students looking for hostel and accommodation information should contact campus administration for the latest approved housing guidance. Availability rules and fee structures may change each semester and should be verified through official UMT channels. Ask for current accommodation options distance from campus and safety arrangements before making commitments. If you need immediate direction send your program and campus details to info@skt.umt.edu.pk to get routed to the relevant office.',
            'accommodation_support'
        ),
        (
            'Academic Regulations and GPA Policy Support',
            'Academic regulations including GPA requirements probation rules attendance policies and progression criteria are governed by official university regulations and handbook policies. Students should review the current handbook and consult their academic advisor for program specific interpretation. If you are worried about low GPA or academic standing seek guidance early from your department and student support offices. Early consultation helps you understand options for improvement and formal procedures.',
            'academic_regulations'
        ),
    ]

    for title, text, category in manual_chunks:
        key = text.strip().lower()
        if key in existing_text:
            continue
        additions.append({
            'group_id': 'G23',
            'chunk_id': f'G23_C{next_id:03d}',
            'topic': 'Campus Support Resources',
            'category': category,
            'risk_level': 'L0_NORMAL',
            'title': title,
            'text': text,
            'source_id': 'S001',
            'allowed_use': 'Official student support routing',
            'blocked_use': 'Unofficial policy guarantees',
            'language': 'English',
        })
        existing_text.add(key)
        next_id += 1

    for title, text in _scrape_chunks():
        key = text.strip().lower()
        if key in existing_text:
            continue
        additions.append({
            'group_id': 'G23',
            'chunk_id': f'G23_C{next_id:03d}',
            'topic': 'UMT Website Updates',
            'category': 'web_resources',
            'risk_level': 'L0_NORMAL',
            'title': title[:120],
            'text': text,
            'source_id': 'S007',
            'allowed_use': 'General campus information and contact routing',
            'blocked_use': 'Unverified or outdated assumptions',
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
