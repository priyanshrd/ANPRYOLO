# Automatic Number Plate Recognition (ANPR)

This repository contains the code and model files for an Automatic Number Plate Recognition (ANPR) system that detects vehicle license plates using YOLOv8 for object detection and EasyOCR for Optical Character Recognition (OCR). The project is optimized for detecting Indian number plates (format: AAAA 99 BB 8765) and can be applied at entry/exit points in institutions to ease vehicle management.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Usage](#usage)
- [Results](#results)
- [Future Work](#future-work)
- [Contributors](#contributors)
- [References](#references)

## Overview
The ANPR system is designed to detect license plates in real-time, even under varying lighting conditions. It leverages YOLOv8’s improved object detection architecture and EasyOCR’s efficient text recognition capabilities to ensure high accuracy and performance. The system achieves an accuracy of **97.8%** on a dataset of 767 labeled images.

## Features
- **High accuracy**: Achieves 97.8% accuracy on the current dataset.
- **Real-time performance**: Uses YOLOv8 and SORT tracking for efficient, real-time tracking.
- **Optimized for Indian License Plates**: Supports Indian format for license plate detection and recognition.
- **Robust OCR**: EasyOCR integrated for fast and accurate character recognition.
- **Handles various lighting conditions**: Image processing steps applied to enhance plate visibility.

## Architecture
1. **Data Collection**: Collection of images from various online datasets.
2. **Preprocessing**: Converts images to grayscale, applies binary inverse thresholding, and crops license plates.
3. **Model Training**: YOLOv8 model trained over 250 epochs (plateaued at 193 epochs).
4. **Object Tracking**: SORT algorithm used for tracking detected plates.
5. **OCR**: EasyOCR extracts characters from detected plates.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/priyanshrd/ANPRYOLO.git
    ```
2. Install dependencies:
    ```bash
    cd ANPRYOLO
    pip install -r requirements.txt
    ```
3. Download pretrained YOLOv8 model weights and place them in the `models` directory.

## Usage
1. Run the main detection script:
    ```bash
    python detect_license_plate.py --input path/to/video.mp4 --output output.csv
    ```
2. Results will be saved as `output.csv`, containing frame number, bounding boxes, car IDs, and license numbers with confidence scores.

## Results
The model demonstrates high accuracy across various test conditions:
- Accuracy: **97.8%**
- Optimal performance on well-lit images and specific camera angles
- Sample processed frames can be found in the `results` directory.

## Future Work
- **Dataset Expansion**: Increase training data for better accuracy across different climates and lighting.
- **DeepSORT Integration**: Enhance tracking for crowded environments.
- **Resolution Improvement**: Use super-resolution techniques for better OCR performance on low-quality images.

## Contributors
- [Dr. H. Pavithra](mailto:pavithrah@rvce.edu.in)
- Priyansh Rajiv Dhotar
- Umang Mishra

## References
- Alex Bewley et al., "Simple Online and Realtime Tracking"
- Comprehensive Review of YOLO Models
- Further references in the `paper/references.pdf`

For detailed information, please refer to the full research paper included in the repository.
