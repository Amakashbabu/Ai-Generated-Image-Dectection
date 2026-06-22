# AI Generated Image Detection

A Deep Learning based system that detects whether an image is Real or AI Generated using EfficientNetB0 and TensorFlow.

## Features

- Real vs AI Generated Image Classification
- EfficientNetB0 Transfer Learning
- Image Preprocessing & Augmentation
- Confidence Score Prediction
- Streamlit Web Application
- Real-Time Detection

## Tech Stack

- Python
- TensorFlow / Keras
- OpenCV
- NumPy
- Streamlit
- EfficientNetB0

## Dataset

CIFAKE Dataset

- 4000 Images
- 2000 Real Images
- 2000 AI Generated Images

## Model

EfficientNetB0 Transfer Learning

Optimizer: Adam

Loss Function: Binary Crossentropy

Batch Size: 32

Epochs: 15-20

## Installation

```bash
git clone https://github.com/yourusername/AI-Generated-Image-Detection.git

cd AI-Generated-Image-Detection

pip install -r requirements.txt

streamlit run app/app.py
