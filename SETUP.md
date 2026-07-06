# Setup Guide — Training Orchidia on Real Orchid Data

Follow these steps once to train the model on the Kaggle orchid dataset,
then upload the project (code + trained model) to GitHub.

## Step 1 — Download the dataset
Download the **20-species orchid dataset** from Kaggle:
https://www.kaggle.com/datasets/mikful/orchids

Extract it so that each species is its own folder inside a `dataset/` folder
in the project root:

```
Orchidia/
├── dataset/
│   ├── Phalaenopsis/   *.jpg
│   ├── Cattleya/       *.jpg
│   ├── Vanda/          *.jpg
│   └── ...             (all 20 species)
├── app.py
├── train.py
└── ...
```
> If the download has `train/` and `valid/` subfolders, point `--data` at the
> folder that directly contains the species folders (see Step 3).

## Step 2 — Install dependencies
```bash
pip install -r requirements.txt
```
For the best (deep-learning) model, also install TensorFlow:
```bash
pip install tensorflow
```

## Step 3 — Train the model (one command)
```bash
python train.py --data dataset
```
- With TensorFlow installed → trains a **MobileNetV2** deep model (best accuracy).
- Without it → automatically trains a lightweight scikit-learn model.

This creates a `model/` folder with the trained model + `classes.json`.

## Step 4 — Run the app
```bash
python app.py
```
Open http://localhost:5000 and upload an orchid photo.

## Step 5 — Upload to GitHub
Commit **everything except the raw dataset** (it's already in `.gitignore`):
- ✅ code, `model/` (trained model), `README.md`, screenshots
- ❌ `dataset/` — too large for GitHub; users retrain from the Kaggle link

That's it — a working, real-data-trained orchid classifier. 🌸
