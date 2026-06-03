import os
from flask import Flask, render_template, request, jsonify
from PIL import Image
import pytesseract

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({'error': 'No image file uploaded'}), 400

    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)

        try:
            img = Image.open(file_path)
            extracted_text = pytesseract.image_to_string(img, lang='eng')
            os.remove(file_path)

            if not extracted_text.strip():
                return jsonify({'text': 'No text could be found in this image. Please try a clearer one.'})

            return jsonify({'text': extracted_text.strip()})

        except Exception as e:
            if os.path.exists(file_path):
                os.remove(file_path)
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)