import pandas as pd
import os
from datetime import datetime

class ExcelExporter:
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
    
    def export_to_excel(self, data, filename=None):
        """Export data to Excel"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'invoice_data_{timestamp}.xlsx'
        
        filepath = os.path.join(self.output_dir, filename)
        df = pd.DataFrame([data])
        df.to_excel(filepath, index=False)
        return filepath
    
    def append_to_excel(self, data, filename='invoices.xlsx'):
        """Append to existing Excel"""
        filepath = os.path.join(self.output_dir, filename)
        df_new = pd.DataFrame([data])
        
        if os.path.exists(filepath):
            df_existing = pd.read_excel(filepath)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_excel(filepath, index=False)
        else:
            df_new.to_excel(filepath, index=False)
        
        return filepath

# Test
if __name__ == "__main__":
    exporter = ExcelExporter()
    sample = {'Invoice Number': 'INV-001', 'Date': '15/08/2024', 'Amount': '$5,000'}
    print(f"✅ Exported to: {exporter.export_to_excel(sample)}")