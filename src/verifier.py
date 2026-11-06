
import re

def verify_phone(phone: str) -> bool:
    if not phone: return False
    digits = re.sub(r"\D", "", phone)
    return len(digits) >= 8

def verify_website(url: str) -> bool:
    if not url: return False
    return url.startswith("http")

def clean_business(data: dict) -> dict:
    # Normalize
    data['Business Name'] = data.get('Business Name','').strip()
    data['Address'] = data.get('Address','').strip()
    data['Phone'] = data.get('Phone','').strip()
    data['Website'] = data.get('Website','').strip()
    data['Verified'] = "Yes" if verify_phone(data['Phone']) else "No"
    return data
