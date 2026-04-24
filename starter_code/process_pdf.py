import google.generativeai as genai
import os
import json

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Use Gemini API to extract structured data from lecture_notes.pdf

def extract_pdf_data(file_path):
    # --- FILE CHECK (Handled for students) ---
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return None
    # ------------------------------------------
    
    # Initialize Gemini API
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set.")
        return None
    
    genai.configure(api_key=api_key)
    
    try:
        # Upload PDF file
        pdf_file = genai.upload_file(path=file_path)
        
        # Initialize model
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt to extract information
        prompt = """Extract the following information from the PDF and return it in JSON format with keys: title, author, summary.
        - Title: The title of the document.
        - Author: The author of the document.
        - Summary: A 3-sentence summary of the document's content."""
        
        # Generate content
        response = model.generate_content([pdf_file, prompt])
        
        # Parse response
        try:
            result = json.loads(response.text)
        except json.JSONDecodeError:
            # If response is not JSON, extract manually
            result = {
                'title': 'Unknown',
                'author': 'Unknown',
                'summary': response.text[:500] if response.text else ''
            }
        
        # Extract fields
        title = result.get('title', 'Unknown')
        author = result.get('author', 'Unknown')
        summary = result.get('summary', '')
        
        # Create content
        content = f"Title: {title}\nAuthor: {author}\nSummary: {summary}"
        
        # Create document dict
        doc = {
            'document_id': 'pdf-lecture-notes',
            'content': content,
            'source_type': 'PDF',
            'author': author,
            'timestamp': None,
            'source_metadata': {
                'title': title,
                'summary': summary
            }
        }
        
        return doc
    
    except Exception as e:
        print(f"Error processing PDF: {e}")
        return None

