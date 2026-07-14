"""
Train Orchidia on a real orchid image dataset.

Expected layout (each subfolder is one class):
    dataset/
        Phalaenopsis/  *.jpg
        Cattleya/      *.jpg
        ...

Usage:
    python train.py --data dataset            # deep learning if TensorFlow is installed
    python train.py --data dataset --sklearn  # force lightweight model
"""
import argparse
import json
import os
import pickle

import numpy as np
from PIL import Image

MODEL_DIR = "model"


def find_classes(data_dir):
    classes = sorted(d for d in os.listdir(data_dir)
                     if os.path.isdir(os.path.join(data_dir, d)))
    if not classes:
        raise SystemExit(f"No class folders found in '{data_dir}'.")
    return classes


def train_sklearn(data_dir, classes):
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    from sklearn.pipeline import Pipeline
    from core.features import extract_features

    X, y = [], []
    for label, cls in enumerate(classes):
        folder = os.path.join(data_dir, cls)
        for f in os.listdir(folder):
            if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp")):
                try:
                    X.append(extract_features(os.path.join(folder, f)))
                    y.append(label)
                except Exception:
                    pass
    X, y = np.array(X), np.array(y)
    print(f"Loaded {len(X)} images across {len(classes)} classes.")
    pipe = Pipeline([("scaler", StandardScaler()),
                     ("rf", RandomForestClassifier(n_estimators=300, random_state=42))])
    pipe.fit(X, y)
    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(os.path.join(MODEL_DIR, "orchid_rf.pkl"), "wb") as f:
        pickle.dump(pipe, f)
    print("Saved model/orchid_rf.pkl")


def train_deep(data_dir, epochs, img):
    import tensorflow as tf
    from tensorflow.keras import layers, models

    train = tf.keras.utils.image_dataset_from_directory(
        data_dir, validation_split=0.2, subset="training", seed=42,
        image_size=(img, img), batch_size=16)
    val = tf.keras.utils.image_dataset_from_directory(
        data_dir, validation_split=0.2, subset="validation", seed=42,
        image_size=(img, img), batch_size=16)
    classes = train.class_names
    print("Classes:", classes)

    base = tf.keras.applications.MobileNetV2(
        input_shape=(img, img, 3), include_top=False, weights="imagenet")
    base.trainable = False

    inputs = layers.Input((img, img, 3))
    x = models.Sequential([layers.RandomFlip("horizontal"),
                           layers.RandomRotation(0.1), layers.RandomZoom(0.1)])(inputs)
    x = tf.keras.applications.mobilenet_v2.preprocess_input(x)
    x = base(x, training=False)
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Dropout(0.3)(x)
    outputs = layers.Dense(len(classes), activation="softmax")(x)
    model = models.Model(inputs, outputs)

    model.compile(optimizer="adam", loss="sparse_categorical_crossentropy", metrics=["accuracy"])
    model.fit(train, validation_data=val, epochs=epochs)

    os.makedirs(MODEL_DIR, exist_ok=True)
    model.save(os.path.join(MODEL_DIR, "orchid_mobilenet.keras"))
    with open(os.path.join(MODEL_DIR, "classes.json"), "w") as f:
        json.dump(list(classes), f)
    print("Saved model/orchid_mobilenet.keras + classes.json")
    return classes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--data", default="dataset")
    ap.add_argument("--epochs", type=int, default=15)
    ap.add_argument("--img", type=int, default=224)
    ap.add_argument("--sklearn", action="store_true", help="force lightweight model")
    args = ap.parse_args()

    classes = find_classes(args.data)
    print(f"Found {len(classes)} classes.")

    use_deep = not args.sklearn
    if use_deep:
        try:
            import tensorflow  # noqa
        except ImportError:
            print("TensorFlow not installed — falling back to the lightweight model.")
            use_deep = False

    if use_deep:
        classes = train_deep(args.data, args.epochs, args.img)
    else:
        train_sklearn(args.data, classes)

    os.makedirs(MODEL_DIR, exist_ok=True)
    with open(os.path.join(MODEL_DIR, "classes.json"), "w") as f:
        json.dump(list(classes), f)
    print(f"\nDone. {len(classes)} orchid species ready. Run: python app.py")


if __name__ == "__main__":
    main()
