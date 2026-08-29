import pytesseract
from PIL import Image, ImageOps, ImageEnhance
import os
import re

class OCREngine:
    def __init__(self):
        if os.name == 'nt':
            tesseract_paths = [
                r'C:\Program Files\Tesseract-OCR\tesseract.exe',
                r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
            ]
            for path in tesseract_paths:
                if os.path.exists(path):
                    pytesseract.pytesseract.tesseract_cmd = path
                    break
    
    def extract_text(self, image_path):
        try:
            image = Image.open(image_path)
            
            # 1. Rotate if sideways
            try:
                osd = pytesseract.image_to_osd(image)
                rotation = int(re.search(r"Rotate: (\d+)", osd).group(1))
                if rotation != 0:
                    image = image.rotate(-rotation, expand=True)
            except:
                pass

            # 2. Preprocess
            image = ImageOps.grayscale(image)
            enhancer = ImageEnhance.Contrast(image)
            image = enhancer.enhance(2.0)

            # 3. THE MAGIC: Use PSM 11 (Sparse text) - handles scattered receipt items!
            custom_config = r'--oem 3 --psm 11'
            text = pytesseract.image_to_string(image, config=custom_config)
            return text.strip()
        except Exception as e:
            return f"Error: {str(e)}"