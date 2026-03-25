import tensorflow as tf
from tensorflow.keras import layers, models
from tensorflow.keras.preprocessing import image_dataset_from_directory
from tensorflow.keras.applications import ResNet50, VGG16
from tensorflow.keras.applications.resnet50 import preprocess_input as resnet_preprocess
from tensorflow.keras.applications.vgg16 import preprocess_input as vgg_preprocess
import pickle

# CONFIG
DATA_DIR = r"C:\Users\vaibh\Downloads\archive\PetImages"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 5

# Load dataset
train_ds = image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

val_ds = image_dataset_from_directory(
    DATA_DIR,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

class_names = train_ds.class_names
print("Classes:", class_names)

AUTOTUNE = tf.data.AUTOTUNE
train_ds = train_ds.prefetch(AUTOTUNE)
val_ds = val_ds.prefetch(AUTOTUNE)

# ---------- RESNET MODEL ----------
def build_resnet():
    base_model = ResNet50(weights="imagenet", include_top=False, input_shape=(224,224,3))
    base_model.trainable = False

    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dense(128, activation="relu")(x)
    output = layers.Dense(1, activation="sigmoid")(x)

    model = models.Model(inputs=base_model.input, outputs=output)

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    return model

# ---------- VGG MODEL ----------
def build_vgg():
    base_model = VGG16(weights="imagenet", include_top=False, input_shape=(224,224,3))
    base_model.trainable = False

    x = base_model.output
    x = layers.Flatten()(x)
    x = layers.Dense(128, activation="relu")(x)
    output = layers.Dense(1, activation="sigmoid")(x)

    model = models.Model(inputs=base_model.input, outputs=output)

    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )
    return model

# Train ResNet
print("\nTraining ResNet...")
resnet_model = build_resnet()
resnet_model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)
pickle.dump(resnet_model, open("resnet50_model.pkl", "wb"))

# Train VGG16
print("\nTraining VGG16...")
vgg_model = build_vgg()
vgg_model.fit(train_ds, validation_data=val_ds, epochs=EPOCHS)
pickle.dump(vgg_model, open("vgg16_model.pkl", "wb"))

print("Models saved successfully!")