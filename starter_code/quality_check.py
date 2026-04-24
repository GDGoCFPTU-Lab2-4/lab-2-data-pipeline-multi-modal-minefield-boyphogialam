# ==========================================
# ROLE 3: OBSERVABILITY & QA ENGINEER
# ==========================================
# Task: Implement quality gates to reject corrupt data or logic discrepancies.

def run_quality_gate(document_dict):
    # Reject documents with 'content' length < 20 characters
    content = document_dict.get('content', '')
    if isinstance(content, str) and len(content) < 20:
        return False
    
    # Reject documents containing toxic/error strings
    if 'Null pointer exception' in content:
        return False
    
    # Flag tax calculation discrepancies (reject if found)
    if document_dict.get('source_type') == 'Code':
        source_metadata = document_dict.get('source_metadata', {})
        if source_metadata.get('has_tax_discrepancy', False):
            return False
    
    return True
