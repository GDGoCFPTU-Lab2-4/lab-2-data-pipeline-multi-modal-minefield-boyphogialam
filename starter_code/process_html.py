from bs4 import BeautifulSoup

# ==========================================
# ROLE 2: ETL/ELT BUILDER
# ==========================================
# Task: Extract product data from the HTML table, ignoring boilerplate.

def parse_html_catalog(file_path):
    # --- FILE READING (Handled for students) ---
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')
    # ------------------------------------------
    
    # Find the main catalog table
    table = soup.find('table', id='main-catalog')
    if not table:
        return []
    
    result = []
    tbody = table.find('tbody')
    if not tbody:
        return []
    
    rows = tbody.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        if len(cols) < 6:
            continue
        
        ma_sp = cols[0].text.strip()
        ten_sp = cols[1].text.strip()
        danh_muc = cols[2].text.strip()
        gia_str = cols[3].text.strip()
        ton_kho_str = cols[4].text.strip()
        danh_gia = cols[5].text.strip()
        
        # Clean price
        price = None
        if gia_str not in ['N/A', 'Liên hệ']:
            cleaned_gia = gia_str.replace(',', '').replace('VND', '').strip()
            try:
                price = float(cleaned_gia)
            except:
                pass
        
        # Clean stock
        stock = None
        if ton_kho_str:
            try:
                stock = int(ton_kho_str)
            except:
                pass
        
        # Create content
        content = f"Product: {ten_sp}, Category: {danh_muc}, Price: {price if price else 'N/A'}, Stock: {stock if stock is not None else 'N/A'}, Rating: {danh_gia}"
        
        # Create document dict
        doc = {
            'document_id': f"html-{ma_sp}",
            'content': content,
            'source_type': 'HTML',
            'author': 'Unknown',
            'timestamp': None,
            'source_metadata': {
                'product_code': ma_sp,
                'product_name': ten_sp,
                'category': danh_muc,
                'price_vnd': price,
                'stock_quantity': stock,
                'rating': danh_gia
            }
        }
        result.append(doc)
    
    return result

