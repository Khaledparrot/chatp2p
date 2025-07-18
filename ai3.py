import os
import cv2
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.utils import to_categorical

# === CONFIGURATION ===
MODEL_PATH = "captcha_model.h5"
IMG_DIR = "imagtest/" 
IMG_WIDTH = 150
IMG_HEIGHT = 80
NUM_DIGITS = 3
NUM_CLASSES = 10

# === Load model ===
print("Loading model...")
model = load_model(MODEL_PATH)
print("Model loaded.")

# === Predict function ===
def predict_image(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        print(f"Failed to read image: {img_path}")
        return None

    if img.shape != (IMG_HEIGHT, IMG_WIDTH):
        print(f"Skipping {img_path} (invalid size: {img.shape})")
        return None

    img = img.astype(np.float32) / 255.0
    img = img.reshape(1, IMG_HEIGHT, IMG_WIDTH, 1)

    preds = model.predict(img)
    digits = [str(np.argmax(p)) for p in preds]
    return "".join(digits)

# === Loop through prediction folder ===
print(f"Scanning folder: {IMG_DIR}")
for fname in os.listdir(IMG_DIR):
    if not fname.lower().endswith(('.png', '.jpg', '.jpeg')):
        continue

    full_path = os.path.join(IMG_DIR, fname)
    prediction = predict_image(full_path)
    if prediction:
        print(f"{fname} → Predicted: {prediction}")
