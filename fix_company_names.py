import sqlite3

def fix_company_names():
    conn = sqlite3.connect('data/internship.db')
    cur = conn.cursor()
    
    mapping = {
        'Infosys Ltd.': 'Infosys',
        'Tata Consultancy Services (TCS)': 'TCS',
        'Wipro Ltd.': 'Wipro',
        'HCL Technologies Ltd.': 'HCL',
        'Google IT Services India Pvt. Ltd.': 'Google',
        'Microsoft India (R&D) Pvt. Ltd.': 'Microsoft',
        'Reliance Industries Ltd.': 'Reliance Industries',
        'HDFC Bank Ltd.': 'HDFC Bank',
        'ICICI Bank Ltd.': 'ICICI Bank',
        'Tata Steel Ltd.': 'Tata Steel'
    }
    
    count = 0
    for old_name, new_name in mapping.items():
        cur.execute("UPDATE applications SET company = ? WHERE company = ?", (new_name, old_name))
        count += cur.rowcount
        
    conn.commit()
    print(f"✅ Successfully updated {count} application records to match HR company names.")
    conn.close()

if __name__ == "__main__":
    fix_company_names()
