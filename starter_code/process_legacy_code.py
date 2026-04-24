import ast
import re

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract docstrings and comments from legacy Python code.

def extract_logic_from_code(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        source_code = f.read()
    # ------------------------------------------
    
    # Parse with AST to get docstrings
    tree = ast.parse(source_code)
    functions = []
    docstrings = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            functions.append(node.name)
            docstring = ast.get_docstring(node)
            if docstring:
                docstrings.append(f"Function {node.name}: {docstring}")
    
    # Extract business rules with regex
    business_rules = re.findall(r'# Business Logic Rule \d+.*', source_code)
    
    # Detect tax discrepancy (comment says 8%, code uses 10%)
    has_tax_discrepancy = False
    if re.search(r'tax_rate = 0\.10', source_code) and re.search(r'8%', source_code, re.IGNORECASE):
        has_tax_discrepancy = True
    
    # Create content
    content_parts = []
    if docstrings:
        content_parts.append("Docstrings:\n" + "\n".join(docstrings))
    if business_rules:
        content_parts.append("Business Rules:\n" + "\n".join(business_rules))
    content = "\n\n".join(content_parts) if content_parts else "No docstrings or business rules found."
    
    # Create document dict
    doc = {
        'document_id': 'legacy-code-001',
        'content': content,
        'source_type': 'Code',
        'author': 'Senior Dev (retired)',
        'timestamp': None,
        'source_metadata': {
            'functions': functions,
            'business_rules': business_rules,
            'has_tax_discrepancy': has_tax_discrepancy
        }
    }
    
    return doc

