from flask import Flask, request, jsonify
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import numpy as np
from PIL import Image
import io

app = Flask(__name__)

# Load the trained .h5 model
try:
    model = load_model('breast_cancer_model.h5')
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def preprocess_image(img):
    # Resize image to match model's expected sizing
    img = img.resize((224, 224))  # Adjust size according to your model's requirements
    
    # Convert to array and preprocess
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = img_array / 255.0  # Normalize pixel values
    
    return img_array

@app.route('/classify', methods=['POST'])
def classify_image():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
        
    try:
        # Check if image file is present in request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'}), 400
        
        # Get the image file from request
        image_file = request.files['image']
        img = Image.open(io.BytesIO(image_file.read()))
        
        # Preprocess the image
        processed_image = preprocess_image(img)
        
        # Make prediction
        prediction = model.predict(processed_image)
        predicted_class = int(np.round(prediction[0][0]))  # Assuming binary classification
        confidence = float(prediction[0][0])
        
        # Return prediction result
        return jsonify({
            'prediction': predicted_class,
            'confidence': confidence,
            'status': 'benign' if predicted_class == 0 else 'malignant'
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

