import os
import json
import pickle
import numpy as np
from PIL import Image

from .features import extract_features
from .orchid_data import CARE_DB, display_name

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


class DemoBackend:
    """Deterministic stand-in used when no trained model is available.

    It maps each image to a stable pseudo-prediction over the known genera so
    the interface is fully explorable out of the box. It performs no real
    classification - the ``demo`` flag makes that explicit in the UI.
    """

    def __init__(self):
        self.classes = [display_name(g) for g in CARE_DB.keys()]

    def predict(self, img):
        small = np.asarray(img.convert("RGB").resize((16, 16)), dtype=np.float64)
        seed = int(np.abs(small).sum()) % (2 ** 32)
        rng = np.random.default_rng(seed)
        logits = rng.random(len(self.classes))
        logits[rng.integers(len(self.classes))] += 3.4  # give it a clear winner
        e = np.exp(logits - logits.max())
        return e / e.sum()


class OrchidClassifier:
    def __init__(self, backend, demo=False):
        self.backend = backend
        self.demo = demo

    def predict(self, img):
        probs = self.backend.predict(img)
        idx = int(np.argmax(probs))
        classes = self.backend.classes
        order = np.argsort(probs)[::-1][:3]
        return {
            "species": classes[idx],
            "confidence": float(probs[idx]),
            "top3": [{"species": classes[i], "prob": float(probs[i])} for i in order],
            "demo": self.demo,
        }


def _load_classes():
    if os.path.exists(CLASSES_PATH):
        with open(CLASSES_PATH) as f:
            return json.load(f)
    return None


def get_classifier():
    """Return the best available classifier.

    Preference order: trained deep model -> trained lightweight model ->
    demo backend. The demo backend guarantees the app always starts, even on a
    fresh clone with no trained model.
    """
    classes = _load_classes()

    if os.path.exists(KERAS_PATH) and classes:
        try:
            import tensorflow as tf
            model = tf.keras.models.load_model(KERAS_PATH)
            return OrchidClassifier(KerasBackend(model, classes))
        except Exception:
            pass

    if os.path.exists(SKLEARN_PATH) and classes:
        with open(SKLEARN_PATH, "rb") as f:
            pipeline = pickle.load(f)
        return OrchidClassifier(SklearnBackend(pipeline, classes))

    # No trained model on disk - fall back to the clearly-labelled demo mode.
    return OrchidClassifier(DemoBackend(), demo=True)
