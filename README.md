<h1 align="center">🌸 Orchidia</h1>
<p align="center"><b>AI-powered orchid identification & intelligent care assistant</b></p>
<p align="center">Upload a photo — Orchidia recognises the orchid species and combines it with live environmental readings to tell you exactly how to care for your plant.</p>

---

## 🌿 Overview

Orchids are as rewarding as they are demanding — each species needs different light, humidity, and watering. **Orchidia** removes the guesswork:

1. 📷 **Identify** — a deep-learning model recognises the orchid species from a photo.
2. 🌡️ **Sense** — the app reads live conditions (temperature, humidity, light).
3. 💡 **Advise** — a care engine compares conditions against that species' ideal ranges and returns clear, actionable guidance and alerts.

Trained on the [20-species orchid dataset](https://www.kaggle.com/datasets/mikful/orchids).

## 📸 Screenshots

<p align="center">
  <img src="docs/screenshot_home.png" width="45%" alt="Home screen" />
  <img src="docs/screenshot_result.png" width="45%" alt="Analysis result" />
</p>

## ✨ Features

- **Species identification** across 20 orchid species
- **Top-3 predictions** with confidence scoring
- **Live sensor evaluation** — temperature, humidity, and light checked against species-specific optimal ranges
- **Smart care alerts** — instant warnings when conditions drift out of range
- **Care library** for 20+ orchid genera — difficulty, watering schedule, expert tips
- **Modern, responsive web UI** — drag-and-drop upload, animated results

## 🧠 How it works

Orchidia uses **transfer learning** — a pretrained **MobileNetV2** network fine-tuned on real orchid photos — to classify species with high accuracy. The prediction feeds a rule-based **care engine** that evaluates live sensor data against each species' ideal environmental ranges.

A lightweight scikit-learn model is included as an automatic fallback when TensorFlow isn't available.

## 🛠️ Tech Stack

`Python` · `TensorFlow (MobileNetV2)` · `Flask` · `scikit-learn` · `NumPy` · `Pillow` · `HTML/CSS/JS`

## 🚀 Quick Start

See **[SETUP.md](SETUP.md)** for full instructions.

```bash
pip install -r requirements.txt
pip install tensorflow        # for the deep model
python train.py --data dataset
python app.py                 # http://localhost:5000
```

## 📁 Project Structure

```
orchidia/
├── app.py                 # Flask web application
├── train.py               # Trains the model on a real dataset
├── core/
│   ├── features.py        # Image feature extraction (fallback model)
│   ├── classifier.py      # Loads deep or lightweight model
│   ├── care_engine.py     # Sensor evaluation & care logic
│   └── orchid_data.py     # Care knowledge base (20+ genera)
├── templates/ · static/   # Web UI
├── SETUP.md               # Step-by-step setup
└── requirements.txt
```

## 🔌 Connecting real sensors

`app.py` simulates sensor readings via `simulate_sensors()`. To use real hardware,
replace that function with input from your sensors (e.g. an Arduino over serial or
an MQTT feed) — the care engine works unchanged.

## 🗺️ Roadmap

- [ ] Fine-tune deeper layers for even higher accuracy
- [ ] Real-time sensor integration (Arduino / ESP32)
- [ ] Watering-schedule notifications
- [ ] Bloom & growth history tracking

---

<p align="center"><i>Built with 🌸 by Nisa Maaşoğlu</i></p>
