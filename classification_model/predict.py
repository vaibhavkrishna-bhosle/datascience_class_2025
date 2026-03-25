import tensorflow as tf
import numpy as np
from tensorflow.keras.preprocessing import image
import pickle

IMG_SIZE = (224, 224)

# Load models
with open("D:\\satyam apps\\datascience_class_2025\\classification_model\\resnet50_model.pkl", "rb") as f:
    resnet_model = pickle.load(f)
# vgg_model = tf.keras.models.load_model("vgg16_model.h5")

CLASS_NAMES = ["Cat", "Dog"]

def preprocess(img_path):
    img = image.load_img(img_path, target_size=IMG_SIZE)
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def predict(model, img_path):
    img = preprocess(img_path)
    pred = model.predict(img)[0][0]
    return CLASS_NAMES[int(pred > 0.5)], pred

# Test image
img_path = "D:\\satyam apps\\datascience_class_2025\\classification_model\\image_1.jpg"

print("\n--- ResNet Prediction ---")
label, conf = predict(resnet_model, img_path)
print(f"Prediction: {label}, Confidence: {conf:.4f}")

# print("\n--- VGG16 Prediction ---")
# label, conf = predict(vgg_model, img_path)
# print(f"Prediction: {label}, Confidence: {conf:.4f}")