import io
import random
from flask import Flask, render_template, request, jsonify
from PIL import Image

from core.classifier import get_classifier
from core.care_engine import evaluate

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 8 * 1024 * 1024

CLASSIFIER = get_classifier()


def simulate_sensors(care):
    def around(rng, spread):
        lo, hi = rng
        return round(random.uniform((lo + hi) / 2 - spread, hi + spread), 1)
    return {
        "temp_c": around(care["ideal"]["temp_c"], 6),
        "humidity_pct": around(care["ideal"]["humidity_pct"], 18),
        "light_lux": int(around(care["ideal"]["light_lux"], 8000)),
    }


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "No image uploaded"}), 400
    try:
        img = Image.open(io.BytesIO(request.files["image"].read()))
    except Exception:
        return jsonify({"error": "Invalid image file"}), 400

    pred = CLASSIFIER.predict(img)
    care = evaluate(pred["species"], {"temp_c": 0, "humidity_pct": 0, "light_lux": 0})
    sensors = simulate_sensors(care)
    care = evaluate(pred["species"], sensors)
    return jsonify({
        "prediction": pred,
        "species_info": {"display_name": care["display_name"], "difficulty": care["difficulty"]},
        "sensors": sensors,
        "care": care,
    })


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
