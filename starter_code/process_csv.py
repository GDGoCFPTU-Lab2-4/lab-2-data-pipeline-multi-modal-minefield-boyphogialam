import pandas as pd
import re

def clean_price(price_str):
    if pd.isna(price_str) or str(price_str).strip() in ['N/A', 'NULL', '']:
        return None
    price_str = str(price_str).strip()
    if price_str.startswith('$'):
        return float(price_str[1:])
    elif price_str.lower() == 'five dollars':
        return 5.0
    else:
        cleaned = price_str.replace(',', '')
        try:
            return float(cleaned)
        except:
            return None

def normalize_date(date_str):
    if pd.isna(date_str):
        return None
    date_str = str(date_str).strip()
    date_str_clean = re.sub(r'(\d+)(th|st|nd|rd)', r'\1', date_str)
    formats = [
        '%Y-%m-%d',
        '%d/%m/%Y',
        '%d-%m-%Y',
        '%Y/%m/%d',
        '%B %d %Y',
        '%d %B %Y',
        '%d %b %Y',
    ]
    for fmt in formats:
        try:
            dt = pd.to_datetime(date_str_clean, format=fmt)
            return dt.strftime('%Y-%m-%d')
        except:
            continue
    try:
        dt = pd.to_datetime(date_str_clean, dayfirst=True)
        return dt.strftime('%Y-%m-%d')
    except:
        return None

def process_sales_csv(file_path):
    # --- FILE READING (Handled for students) ---
    df = pd.read_csv(file_path)
    # ------------------------------------------
    
    # Remove duplicate rows based on 'id'
    df = df.drop_duplicates(subset='id', keep='first')
    
    # Clean 'price' column
    df['price'] = df['price'].apply(clean_price)
    
    # Normalize 'date_of_sale' into YYYY-MM-DD
    df['date_of_sale'] = df['date_of_sale'].apply(normalize_date)
    
    result = []
    for _, row in df.iterrows():
        # Handle stock_quantity
        stock = row['stock_quantity']
        if pd.isna(stock):
            stock = None
        else:
            try:
                stock = int(stock)
            except:
                stock = None
        
        # Create content
        content = f"Product: {row['product_name']}, Category: {row['category']}, Price: {row['price'] if row['price'] is not None else 'N/A'}, Date: {row['date_of_sale'] if row['date_of_sale'] else 'N/A'}, Seller ID: {row['seller_id']}, Stock: {stock if stock is not None else 'N/A'}"
        
        # Create document dict
        doc = {
            'document_id': f"csv-{row['id']}",
            'content': content,
            'source_type': 'CSV',
            'author': 'Unknown',
            'timestamp': None,
            'source_metadata': {
                'product_id': row['id'],
                'product_name': row['product_name'],
                'category': row['category'],
                'price': row['price'],
                'currency': row['currency'],
                'date_of_sale': row['date_of_sale'],
                'seller_id': row['seller_id'],
                'stock_quantity': stock
            }
        }
        result.append(doc)
    
    return result

