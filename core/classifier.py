import os
import json
import pickle
import numpy as np
from PIL import Image

from .features import extract_features

MODEL_DIR = os.path.join(os.path.dirname(__file__), "..", "model")
SKLEARN_PATH = os.path.join(MODEL_DIR, "orchid_rf.pkl")
KERAS_PATH = os.path.join(MODEL_DIR, "orchid_mobilenet.keras")
CLASSES_PATH = os.path.join(MODEL_DIR, "classes.json")


class SklearnBackend:
    def __init__(self, pipeline, classes):
        self.pipeline, self.classes = pipeline, classes

    def predict(self, img):
        probs = self.pipeline.predict_proba(extract_features(img).reshape(1, -1))[0]
        return probs


class KerasBackend:
    def __init__(self, model, classes):
        self.model, self.classes = model, classes
        import tensorflow as tf
        self.tf = tf

    def predict(self, img):
        arr = np.asarray(img.convert("RGB").resize((224, 224)), dtype=np.float32)
        arr = self.tf.keras.applications.mobilenet_v2.preprocess_input(arr)
        return self.model.predict(arr[None, ...], verbose=0)[0]


class OrchidClassifier:
    def __init__(self, backend):
        self.backend = backend

    def predict(self, img):
        probs = self.backend.predict(img)
        idx = int(np.argmax(probs))
        classes = self.backend.classes
        order = np.argsort(probs)[::-1][:3]
        return {
            "species": classes[idx],
            "confidence": float(probs[idx]),
            "top3": [{"species": classes[i], "prob": float(probs[i])} for i in order],
        }


def _load_classes():
    if os.path.exists(CLASSES_PATH):
        with open(CLASSES_PATH) as f:
            return json.load(f)
    return None


def get_classifier():
    classes = _load_classes()
    # Prefer the deep model if it and TensorFlow are available
    if os.path.exists(KERAS_PATH) and classes:
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(KERAS_PATH)
            return OrchidClassifier(KerasBackend(model, classes))
        except Exception:
            pass
    # Otherwise use the scikit-learn model
    if os.path.exists(SKLEARN_PATH) and classes:
        with open(SKLEARN_PATH, "rb") as f:
            pipeline = pickle.load(f)
        return OrchidClassifier(SklearnBackend(pipeline, classes))
    raise RuntimeError(
        "No trained model found. Run 'python train.py --data dataset' first "
        "(see SETUP.md)."
    )
