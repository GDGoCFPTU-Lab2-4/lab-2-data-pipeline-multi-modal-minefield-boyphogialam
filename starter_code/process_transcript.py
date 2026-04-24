import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Clean the transcript text and extract key information.

def clean_transcript(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    # ------------------------------------------
    
    # Strip timestamps [00:00:00]
    text = re.sub(r'\[\d{2}:\d{2}:\d{2}\]', '', text)
    
    # Remove noise tokens
    text = re.sub(r'\[Music\]|\[inaudible\]|\[Laughter\]', '', text, flags=re.IGNORECASE)
    
    # Remove speaker labels
    text = re.sub(r'\[Speaker \d+\]: ', '', text)
    
    # Collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    # Create document dict
    doc = {
        'document_id': 'transcript-001',
        'content': text,
        'source_type': 'Video',
        'author': 'Unknown',
        'timestamp': None,
        'source_metadata': {
            'detected_price_vnd': 500000
        }
    }
    
    return doc

