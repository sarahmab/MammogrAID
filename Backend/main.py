from flask import Flask, request, jsonify
import torch
from torchvision import transforms
from PIL import Image
import io
import numpy as np

app = Flask(__name__)

# Load the trained PyTorch model
try:
    model = torch.load('breast_cancer_model.pt')
    model.eval()  # Set model to evaluation mode
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def preprocess_image(img):
    # Define image transformations
    preprocess = transforms.Compose([
        transforms.Resize((224, 224)),  # Resize image
        transforms.ToTensor(),  # Convert to tensor
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])  # Normalize
    ])
    
    # Apply transformations
    img_tensor = preprocess(img)
    img_tensor = img_tensor.unsqueeze(0)  # Add batch dimension
    
    return img_tensor

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
        with torch.no_grad():
            prediction = model(processed_image)
            predicted_prob = torch.sigmoid(prediction)  # Assuming binary classification
            predicted_class = (predicted_prob >= 0.5).int().item()
            confidence = predicted_prob.item()
        
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
