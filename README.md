# 🧠 AutoTumorAI: Automated Kidney Tumor Detection from CT Scans

## 🚀 Overview

**AutoTumorAI** is a deep learning-based solution to assist radiologists and healthcare professionals in detecting **kidney tumors** from **CT scan images**. It aims to reduce diagnostic delays by providing **automated, accurate, and fast predictions** using a trained VGG16 model via **transfer learning**.

This project features a complete **ML pipeline**, integrates **MLOps tools** like **DVC**, **MLflow**, and **DagsHub** for versioning and experiment tracking, and includes a **Flask web application** for real-time tumor detection.

---

## 🎯 Objective

Address the challenge of time-consuming and error-prone kidney tumor diagnoses by:
- Automating detection from CT scan images.
- Improving accuracy and reproducibility using MLOps practices.
- Providing a simple web interface for live predictions.

---

## 🧰 Tech Stack

| Category              | Tools / Frameworks                                  |
|----------------------|------------------------------------------------------|
| Programming Language  | Python                                              |
| Deep Learning         | TensorFlow, VGG16 (Transfer Learning)               |
| Version Control       | Git, DVC (Data Version Control)                     |
| Experiment Tracking   | MLflow                                              |
| Collaboration         | DagsHub                                             |
| Web Application       | Flask                                               |

---

## 📈 Results

- ✅ **Achieved Accuracy:** **86%** on the validation dataset.
- 🧪 Demonstrated strong generalization performance on unseen CT scan images.
- 📦 Fully reproducible with pipeline versioning and experiment logging.

---

## 🧪 ML Pipeline Components

1. **Data Ingestion** – Structured folder-based dataset (train/test).
2. **Data Versioning** – Managed using **DVC** with remote storage via **DagsHub**.
3. **Model Building** – Based on **VGG16** with custom layers.
4. **Model Training** – Fine-tuned and evaluated using TensorFlow.
5. **Experiment Tracking** – Logged metrics and parameters with **MLflow**.
6. **Model Evaluation** – Assessed using accuracy and confusion matrix.
7. **Web Deployment** – Real-time prediction via a Flask-based interface.

---

## 🖥️ Web App Demo

The web interface allows users to:
- Upload CT scan images.
- Receive tumor/no-tumor predictions in real time.

---

## 📁 Folder Structure
```
AutoTumorAI/
│
├── data/                   # CT Scan Images (managed by DVC)
├── src/                    # Model training, evaluation, and utils
├── templates/              # HTML templates for Flask app
├── static/                 # CSS and JS files
├── app.py                  # Flask application
├── dvc.yaml                # DVC pipeline definition
├── params.yaml             # Model and training configuration
├── README.md               # Project documentation
└── requirements.txt        # Required dependencies
```

---

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/dipti-55/AutoTumorAI.git
cd AutoTumorAI

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

---

## 📌 Future Improvements

* Expand to multi-class tumor classification.
* Integrate user authentication for clinical usage.
* Deploy on cloud (Heroku, AWS, etc.).
