"""Tests for Orchidia.

Everything here runs without TensorFlow or the Kaggle dataset: the care logic
is pure Python, and the classifier is exercised through its demo backend, so the
suite is fast and CI-friendly.
"""

import io

import numpy as np
from PIL import Image

from core.orchid_data import CARE_DB, care_for, display_name
from core.care_engine import evaluate
from core.features import extract_features, FEATURE_DIM
from core.classifier import get_classifier, DemoBackend, OrchidClassifier


def _sample_image(color=(150, 90, 160)):
    return Image.new("RGB", (200, 200), color)


# --- Care knowledge base -------------------------------------------------

def test_care_db_is_complete():
    assert len(CARE_DB) == 20
    for genus, profile in CARE_DB.items():
        for key in ("difficulty", "temp_c", "humidity_pct", "light_lux", "water_days", "desc", "tips"):
            assert key in profile, f"{genus} missing {key}"
        assert profile["tips"], f"{genus} has no tips"


def test_care_for_matches_by_substring():
    assert care_for("Phalaenopsis amabilis")["matched_genus"] == "phalaenopsis"
    assert care_for("Cattleya_labiata")["matched_genus"] == "cattleya"


def test_care_for_unknown_falls_back_to_default():
    care = care_for("Totally Unknown Plant")
    assert care["matched_genus"] is None
    assert care["difficulty"] == "Intermediate"


def test_display_name_is_readable():
    assert display_name("phalaenopsis_amabilis") == "Phalaenopsis Amabilis"


# --- Care engine ---------------------------------------------------------

def test_evaluate_flags_out_of_range_conditions():
    result = evaluate("phalaenopsis", {"temp_c": 40, "humidity_pct": 10, "light_lux": 100})
    assert result["status"] == "critical"
    assert len(result["warnings"]) >= 2
    assert result["description"]


def test_evaluate_reports_healthy_in_ideal_range():
    result = evaluate("phalaenopsis", {"temp_c": 23, "humidity_pct": 60, "light_lux": 15000})
    assert result["status"] == "healthy"
    assert result["warnings"] == []


def test_evaluate_returns_all_three_checks():
    result = evaluate("vanda", {"temp_c": 25, "humidity_pct": 70, "light_lux": 30000})
    metrics = {c["metric"] for c in result["checks"]}
    assert metrics == {"Temperature", "Humidity", "Light"}


# --- Feature extraction --------------------------------------------------

def test_features_have_stable_dimension():
    feats = extract_features(_sample_image())
    assert feats.shape == (FEATURE_DIM,)
    assert np.isfinite(feats).all()


# --- Classifier / demo mode ---------------------------------------------

def test_get_classifier_falls_back_to_demo():
    clf = get_classifier()
    assert isinstance(clf, OrchidClassifier)
    assert clf.demo is True  # no trained model present in the test environment


def test_demo_prediction_shape_and_determinism():
    clf = OrchidClassifier(DemoBackend(), demo=True)
    img = _sample_image()
    a = clf.predict(img)
    b = clf.predict(img)
    assert a["species"] == b["species"]           # deterministic per image
    assert 0.0 <= a["confidence"] <= 1.0
    assert len(a["top3"]) == 3
    assert a["demo"] is True


def test_different_images_can_differ():
    clf = OrchidClassifier(DemoBackend(), demo=True)
    preds = {clf.predict(_sample_image((c, c, c)))["species"] for c in (20, 90, 160, 230)}
    assert len(preds) >= 2  # not everything collapses to one class


# --- API -----------------------------------------------------------------

def test_analyze_endpoint_end_to_end():
    from app import app

    img = _sample_image()
    buf = io.BytesIO(); img.save(buf, "JPEG"); buf.seek(0)
    client = app.test_client()

    assert client.get("/health").get_json()["status"] == "ok"

    r = client.post("/analyze", data={"image": (buf, "orchid.jpg")},
                    content_type="multipart/form-data")
    assert r.status_code == 200
    d = r.get_json()
    assert d["prediction"]["demo"] is True
    assert d["species_info"]["description"]
    assert len(d["care"]["checks"]) == 3


def test_analyze_rejects_missing_image():
    from app import app

    r = app.test_client().post("/analyze", data={}, content_type="multipart/form-data")
    assert r.status_code == 400
