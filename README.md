# Gesture Mouse Control

![Language](https://img.shields.io/badge/language-Python-blue)
![Framework](https://img.shields.io/badge/framework-OpenCV-green)
![Library](https://img.shields.io/badge/library-MediaPipe-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Release](https://img.shields.io/github/v/release/AlbertoMarquillas/gesture-mouse-control)
![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow)

---

## 📌 Overview

The **Gesture Mouse Control** project demonstrates how to use **hand-tracking with OpenCV and MediaPipe** to emulate system actions using real-time hand gestures. In this implementation, the gestures are mapped to **volume control**, but the framework can be extended to emulate other mouse or keyboard actions.

The project showcases how computer vision and human–computer interaction can be combined to build natural and intuitive interfaces.

---

## 📂 Repository Structure

```
<repo>/
├─ src/                     # Source code
│  ├─ main.py               # Entry point: runs the volume control app
│  └─ hand_tracking_module.py # Hand tracking module (mediapipe wrapper)
├─ test/                    # Placeholder for future tests
├─ docs/                    # Documentation and assets
│  └─ assets/               # Figures, screenshots, diagrams
├─ notebooks/               # Optional experimentation notebooks
├─ build/                   # Temporary outputs (ignored)
├─ requirements.txt         # Dependencies
└─ README.md                # Project documentation
```

---

## ⚙️ Installation

Ensure you have **Python 3.9+**. Install the dependencies listed in `requirements.txt`:

```powershell
git clone https://github.com/AlbertoMarquillas/gesture-mouse-control.git
cd gesture-mouse-control
pip install -r requirements.txt
```

Typical dependencies include:

* `opencv-python`
* `mediapipe`
* `numpy`

---

## 🚀 Usage

Run the application from the command line:

```powershell
python src/main.py
```

* The webcam feed will open.
* The **hand landmarks** are detected in real time.
* Gestures (e.g., distance between thumb and index fingers) are mapped to **system volume control**.

> ⚠️ Note: the current implementation modifies system volume. To extend it for **mouse control** or **other actions**, adjust the mapping logic inside `main.py`.

---

## 🔍 Features

* **Real-time hand tracking** using **MediaPipe**.
* **Gesture recognition** mapped to system actions.
* **Volume control demo** included by default.
* Modular code: `hand_tracking_module.py` encapsulates the MediaPipe logic.
* Easily extendable to support other gestures and actions.

---

## 📚 What I Learned

Through this project I gained experience in:

* Using **OpenCV** for real-time video processing.
* Applying **MediaPipe** for robust hand-tracking.
* Mapping geometric relationships (distance between landmarks) to actionable commands.
* Designing intuitive human–computer interaction prototypes.
* Structuring Python projects for clarity and reusability.

---

## 📜 License

This project is released under the [MIT License](LICENSE).
