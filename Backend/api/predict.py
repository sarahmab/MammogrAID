import numpy as np
from flask import Flask, request, jsonify
from utils import load_and_preprocess_image, model
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/predict', methods=['POST'])
def handler():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    image_file = request.files['image']
    image_data = image_file.read()
    
    img_array = load_and_preprocess_image(image_data)
    
    if img_array is not None:
        img_batch = np.expand_dims(img_array, axis=0)
        predictions = model.predict(img_batch)
        
        cancer_probability = float(predictions[0][0])  # Convert to Python float for JSON serialization
        predicted_class = "Cancer" if cancer_probability >= 0.5 else "Normal"
        
        return jsonify({
            'predicted_class': predicted_class,
            'cancer_probability': cancer_probability
        })
    else:
        return jsonify({'error': 'Image processing failed'}), 400
    
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'})

@app.route('/api/test', methods=['GET'])
def test():
    return "jsonify({'status': 'Backend is connected!'})"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
