import re

class InvoiceExtractor:
    def extract_all(self, text):
        data = {
            'invoice_number': self.extract_invoice_number(text),
            'date': self.extract_date(text),
            'amount': self.extract_amount(text),
            'vendor': self.extract_vendor(text)
        }
        return data

    def extract_invoice_number(self, text):
        # 1. Look specifically for "Receipt:" or "Invoice" followed by text (Best for clear receipts)
        patterns = [
            r'(?:Receipt|Invoice|Inv)\s*[:#]?\s*([A-Za-z0-9-]+)', 
            # 2. Look for long alpha-numeric strings
            r'\b[a-zA-Z]{1,5}\d{6,15}[a-zA-Z]{1,5}\b',
            # 3. Look for long digit strings
            r'\b\d{10,15}\b',
            # 4. Last resort: phone numbers or dashed numbers
            r'\(\d{1,3}\)\s?\d{7,10}', 
            r'\b\d{2,5}-\d{2,5}\b'     
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1) if match.groups() else match.group(0).replace(" ", "")
        return "Not found"

    def extract_date(self, text):
        # Look for dates anywhere in the text
        patterns = [
            # Catches "Date: 2ag9-11-2" or "Date: 61/9)"
            r'(?:Date|Dat)\s*[:#]?\s*([\d\s/.\-]+)',
            # Catches standard dates
            r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', 
            # Catches "3/17"
            r'\b\d{1,2}[-/]\d{1,2}\b'
        ]
        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                # If it's from the "Date:" label, remove spaces
                if match.groups():
                    return match.group(1).strip().replace(" ", "")
                else:
                    return match.group(0)
        return "Not found"

    def extract_amount(self, text):
        pattern = r'\b\d{1,3}(?:,\d{3})*(?:\.\d{2})\b|\b\d+\.\d{2}\b'
        matches = re.findall(pattern, text)
        if matches:
            amounts = [float(m.replace(',', '')) for m in matches]
            return f"{max(amounts):.2f}"
        return "Not found"

    def extract_vendor(self, text):
        # Catch "Landing Apt", "Kelseyburgh", "Williamss", "Clayton", etc.
        patterns = [
            r'\b[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*\s(?:Inc|LLC|Ltd|Corp|Supplies|Stores|Company|Services|Apt)\b',
            r'\b[A-Z][a-zA-Z]+(?:\s[A-Z][a-zA-Z]+)*'
        ]
        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(0).strip()
        return "Not found"