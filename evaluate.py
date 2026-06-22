import csv
import time
from pathlib import Path

from app import app


BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / 'group_23_campus_support_resources'
QUESTIONS_PATH = DATA_DIR / '3_benchmark_questions.csv'
OUTPUT_PATH = DATA_DIR / '6_model_responses.csv'
SYSTEMS = ['S0', 'S1', 'S2']
# S3 is intentionally excluded from batch evaluation because it depends on optional API credentials.


def run():
    with QUESTIONS_PATH.open('r', encoding='utf-8', newline='') as f:
        questions = list(csv.DictReader(f))

    rows = []
    with app.test_client() as client:
        for q in questions:
            question_id = q['question_id']
            user_question = q['user_question']

            for system in SYSTEMS:
                start = time.perf_counter()
                response = client.post('/chat', json={'message': user_question, 'system': system})
                elapsed = time.perf_counter() - start

                payload = response.get_json() or {}
                chunks = payload.get('retrieved_chunks') or []
                chunk_str = ';'.join(str(c) for c in chunks)

                rows.append({
                    'question_id': question_id,
                    'system_type': system,
                    'response': payload.get('response', ''),
                    'retrieved_chunk_ids': chunk_str,
                    'response_time_seconds': f'{elapsed:.4f}'
                })

    with OUTPUT_PATH.open('w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                'question_id',
                'system_type',
                'response',
                'retrieved_chunk_ids',
                'response_time_seconds'
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f'Wrote {len(rows)} rows to {OUTPUT_PATH}')


if __name__ == '__main__':
    run()
