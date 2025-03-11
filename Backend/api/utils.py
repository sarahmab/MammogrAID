from flask import app, jsonify, request
from huggingface_hub import hf_hub_download
import tensorflow as tf
import cv2
import numpy as np
import json
from PIL import Image
import io
from flask_cors import CORS

# Load model
repo_id = "maiurilorenzo/CBIS-DDSM-CNN"
model_path = hf_hub_download(repo_id=repo_id, filename="CNN_model.h5")
model = tf.keras.models.load_model(model_path)

# Load preprocessing info
preprocessing_path = hf_hub_download(repo_id=repo_id, filename="preprocessing.json")
with open(preprocessing_path, "r") as f:
    preprocessing_info = json.load(f)

def load_and_preprocess_image(image_data):
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(image_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        if img is None:
            raise ValueError("Could not decode image")
        
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, tuple(preprocessing_info["target_size"]), interpolation=cv2.INTER_AREA)
        img_array = img.astype(np.float32) / 255.0

        return img_array
    except Exception as e:
        print(f"Error processing image: {str(e)}")
        return None