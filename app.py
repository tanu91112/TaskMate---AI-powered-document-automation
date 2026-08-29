import os
import tempfile
from flask import Flask, request, render_template, send_file, jsonify
from werkzeug.utils import secure_filename
import json

from ocr_engine import OCREngine
from extractor import InvoiceExtractor
from exporter import ExcelExporter

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ocr = OCREngine()
extractor = InvoiceExtractor()
exporter = ExcelExporter()

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        text = ocr.extract_text(filepath)
        print("=" * 50)
        print("🔍 EXTRACTED TEXT FROM IMAGE:")
        print("=" * 50)
        print(text)
        print("=" * 50)
        extracted_data = extractor.extract_all(text)
                
        return jsonify({
            'success': True,
            'extracted_text': text,
            'data': extracted_data
        })
    
    return jsonify({'error': 'Invalid file type'}), 400

@app.route('/export', methods=['POST'])
def export():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    filepath = exporter.export_to_excel(data)
    return jsonify({
        'success': True,
        'filepath': filepath,
        'download_url': '/download/' + os.path.basename(filepath)
    })

@app.route('/download/<filename>')
def download(filename):
    filepath = os.path.join(exporter.output_dir, filename)
    if os.path.exists(filepath):
        return send_file(filepath, as_attachment=True)
    return jsonify({'error': 'File not found'}), 404

if __name__ == '__main__':
    print("🚀 TaskMate - Document to Task Automation")
    print("📁 Open in browser: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)