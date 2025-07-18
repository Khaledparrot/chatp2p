import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.callbacks import ModelCheckpoint

# === CONFIGURATION ===
IMG_DIR = "captchas/"
IMG_WIDTH = 150
IMG_HEIGHT = 80
NUM_DIGITS = 3
NUM_CLASSES = 10

# === Load and preprocess data ===
def load_data():
    X = []
    y = []
    bad = 0
    print("🔍 Loading images and labels...")
    for filename in os.listdir(IMG_DIR):
        if 'nyo' in filename.lower():
            continue
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            label = filename.split('.')[0][:3]
            if len(label) != NUM_DIGITS or not label.isdigit():
                bad += 1
                continue
            img_path = os.path.join(IMG_DIR, filename)
            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            if img is None or img.shape != (IMG_HEIGHT, IMG_WIDTH):
                bad += 1
                continue
            img = img.astype(np.float32) / 255.0
            X.append(img)
            y.append([int(d) for d in label])
    print(f"✅ Loaded {len(X)} clean images.")
    print(f"🗑️ Skipped {bad} bad images.")
    return np.array(X), np.array(y)

# === Load and preprocess ===
X, y = load_data()
X = X.reshape(-1, IMG_HEIGHT, IMG_WIDTH, 1)

# === One-hot encode labels ===
print("🧠 One-hot encoding labels...")
y_encoded = [to_categorical(y[:, i], num_classes=NUM_CLASSES) for i in range(NUM_DIGITS)]

# === Debug info ===
print("🔎 Verifying label shapes...")
print(f"Total images: {X.shape[0]}")
for i, d in enumerate(y_encoded):
    print(f"Digit {i+1} labels shape: {d.shape}")

# === Train-test split ===
print("🧠 Splitting data into training and validation sets...")
X_train, X_val, y1_train, y1_val, y2_train, y2_val, y3_train, y3_val = train_test_split(
    X, y_encoded[0], y_encoded[1], y_encoded[2],
    test_size=0.1, random_state=42
)
y_train = [y1_train, y2_train, y3_train]
y_val = [y1_val, y2_val, y3_val]

# === Build the model ===
print("🛠️ Building the model...")
inputs = Input(shape=(IMG_HEIGHT, IMG_WIDTH, 1))
x = Conv2D(32, (3, 3), activation='relu', padding='same')(inputs)
x = MaxPooling2D((2, 2))(x)
x = Conv2D(64, (3, 3), activation='relu', padding='same')(x)
x = MaxPooling2D((2, 2))(x)
x = Flatten()(x)

digit_outputs = [Dense(NUM_CLASSES, activation='softmax', name=f'digit{i+1}')(x) for i in range(NUM_DIGITS)]

model = Model(inputs=inputs, outputs=digit_outputs)
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# === Train the model ===
print("📚 Training the model...")
model.summary()
history = model.fit(
    X_train, y_train,
    validation_data=(X_val, y_val),
    batch_size=32,
    epochs=20,
    callbacks=[ModelCheckpoint("captcha_model.h5", save_best_only=True)],
    verbose=2
)

# === Final accuracy report ===
print("\n✅ Final Accuracy Per Digit:")
for i in range(NUM_DIGITS):
    train_acc = history.history[f'digit{i+1}_accuracy'][-1] * 100
    val_acc = history.history[f'val_digit{i+1}_accuracy'][-1] * 100
    print(f"Digit {i+1}: Train {train_acc:.2f}% | Val {val_acc:.2f}%")

print("\n💾 Model saved as captcha_model.h5")
