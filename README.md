<div align="center">
  <br />

# ASCII Camera with AI Tracking

**Real-time ASCII Art Generation using Computer Vision and Machine Learning**

Transform your webcam feed into a dynamic matrix of characters in real-time. This project goes beyond simple pixel-to-text mapping by incorporating background segmentation and hand tracking.

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8%2B-red?style=for-the-badge&logo=opencv&logoColor=white)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10%2B-green?style=for-the-badge&logo=google&logoColor=white)](https://developers.google.com/mediapipe)

</div>

<br />

## About The Project

This application captures your webcam video and renders it directly onto your terminal or display using ASCII characters. By leveraging Google's **MediaPipe** library, it features advanced background segmentation (removing your background before converting to ASCII) and hand tracking (highlighting hands over the ASCII feed).

---

## Features

- **Real-Time ASCII Rendering**: High-performance conversion of video frames to characters.
- **Background Segmentation**: Uses AI to isolate the person and remove the background, ensuring cleaner ASCII art.
- **Hand Tracking**: Overlays skeletal hand tracking on top of the character matrix.
- **Configurable Matrix**: Tweak contrast, brightness, character sets, and resolution directly from the configuration files.
- **Modular Design**: Clean code architecture separating capture, processing, AI models, and rendering logic.

---

## Architecture

```text
camera/
|-- start_camera.bat           # Quick launch script
|-- ascii_camera/
|   |-- main.py                # Main application loop
|   |-- camera.py              # Handles video capture streams
|   |-- ascii_converter.py     # Maps brightness to characters
|   |-- segmentation.py        # MediaPipe background removal
|   |-- hand_tracking.py       # MediaPipe hand landmarks
|   |-- renderer.py            # Console/Terminal drawing logic
|   `-- config.json            # User preferences and thresholds
```

---

## Installation & Setup

### Prerequisites
Make sure you have Python 3.10 or higher installed.

### Step 1: Install Dependencies
Open your terminal inside the `ascii_camera` folder and run:
```bash
pip install -r requirements.txt
```
This will install `opencv-python`, `numpy`, and `mediapipe`.

### Step 2: Run the Camera
You can start the ASCII camera by either double-clicking the `start_camera.bat` script, or by running the main python file directly:
```bash
python ascii_camera/main.py
```

---

## Customization

You can edit `config.json` (or `config.py`) to change how the application renders:
- **Character Set**: Change the string of characters used from dark to light.
- **Resolution**: Lower the output width/height for better performance or denser art.
- **Toggle Features**: Enable or disable background removal and hand tracking individually.

---

<div align="center">
  <br/>
  <b>Built for terminal enthusiasts and computer vision learners.</b>
</div>
