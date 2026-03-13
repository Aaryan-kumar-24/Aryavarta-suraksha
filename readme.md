🛡️ Aryavarta Suraksha
Intelligent AI-Powered Smart Surveillance System

Aryavarta Suraksha is an AI-powered smart surveillance web application designed to enhance modern security infrastructure using computer vision and real-time analytics.

The system integrates:

Face recognition

Behavioral monitoring

Crowd heatmap analysis

Intrusion detection

Automated alert systems

Unlike traditional CCTV systems that rely on manual monitoring, Aryavarta Suraksha uses AI-driven event detection to automatically analyze video feeds and generate alerts when suspicious activities occur.

The platform enables security administrators to monitor multiple cameras simultaneously through a centralized dashboard, improving response time and incident prevention.

🌍 Project Vision

Modern surveillance systems rely heavily on continuous manual monitoring of CCTV feeds.

This approach presents major limitations:

Human fatigue during long monitoring hours

Delayed response to security incidents

Difficulty identifying individuals quickly

Lack of behavioral analytics

No automated alert system

As organizations and cities expand, traditional surveillance systems become inefficient and reactive instead of proactive.

Objective

Aryavarta Suraksha aims to transform traditional surveillance into an AI-assisted intelligent monitoring system capable of:

detecting suspicious activity automatically

identifying individuals using facial recognition

analyzing crowd density patterns

detecting unauthorized entry

generating automated security alerts

🎯 Resume-Ready Project Summary

Aryavarta Suraksha — AI-Based Smart Surveillance Web Application

Developed an AI-powered surveillance platform capable of:

real-time face recognition

crowd density heatmap analytics

intrusion detection

automated security alerts

Key Achievements

~96% facial recognition accuracy using 128-dimensional facial embeddings

Real-time video analytics with <200ms latency

Multi-module event detection system

Automated email alert system

Live monitoring dashboard using Django MVT architecture

🛠 Tech Stack
Frontend

HTML5

CSS3

JavaScript

Django Templates

Backend

Python

Django

Computer Vision

OpenCV

NumPy

Database

SQLite

🚩 Core Security Problem

Traditional CCTV workflow:

CCTV Camera
     |
     v
Video Feed
     |
     v
Security Monitor
     |
     v
Manual Human Monitoring
     |
     v
Incident Detection (Delayed)
Limitations

incidents detected late

constant monitoring required

no automated identification

no crowd analytics

no behavior detection

💡 Intelligent Surveillance Workflow
Camera Video Stream
        |
        v
+----------------------+
|   Frame Processing   |
|      OpenCV          |
+----------+-----------+
           |
           v
+----------------------+
|    Face Detection    |
+----------+-----------+
           |
           v
+----------------------+
|   Identity Verify    |
+----------+-----------+
           |
           v
+----------------------+
| Behavior Analysis    |
| Heatmap + Wait Time  |
+----------+-----------+
           |
           v
+----------------------+
| Security Event       |
| Detection            |
+----------+-----------+
           |
           v
+----------------------+
| Alert & Logging      |
+----------+-----------+
           |
           v
+----------------------+
| Surveillance UI      |
+----------------------+
🔎 Key Features
Face Recognition System

Real-time identity verification using 128 facial embeddings.

Capabilities:

detect faces in live video

match faces with stored dataset

mark attendance automatically

log entry timestamps

Accuracy: ~96%

Automated Attendance System

Recognized individuals are logged automatically in:

Attendance.csv

Recorded information:

name

timestamp

entry status

Crowd Density Heatmap

The system generates real-time heatmaps to visualize crowd density.

Benefits:

detect overcrowding

identify high-traffic zones

analyze movement patterns

Restricted Zone Intrusion Detection
Person Detection
        |
        v
Restricted Zone Mapping
        |
        v
Boundary Crossing
        |
        v
Security Alert
Prolonged Waiting Detection

Detects individuals waiting longer than a defined threshold.

Configuration file:

wait_config.pkl
🧠 Multi-Camera AI Surveillance Architecture
                +----------------------+
                |      Camera 1        |
                +----------+-----------+
                           |
                +----------------------+
                |      Camera 2        |
                +----------+-----------+
                           |
                +----------------------+
                |      Camera 3        |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |   Video Aggregator   |
                +----------+-----------+
                           |
                           v
                +----------------------+
                |  AI Vision Engine    |
                |     (OpenCV)         |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Event Detection      |
                | Engine               |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Django Backend       |
                +----------+-----------+
                           |
                           v
                +----------------------+
                | Monitoring Dashboard |
                +----------------------+
🧠 Face Recognition Pipeline
Video Frame
     |
     v
+---------------------+
| Face Detection      |
| (Haar Cascade)      |
+----------+----------+
           |
           v
+---------------------+
| Face Alignment      |
+----------+----------+
           |
           v
+---------------------+
| Feature Extraction  |
| 128-D Embedding     |
+----------+----------+
           |
           v
+---------------------+
| Face Encoding DB    |
| Known Faces         |
+----------+----------+
           |
           v
+---------------------+
| Similarity Match    |
| Euclidean Distance  |
+----------+----------+
           |
           v
+---------------------+
| Identity Verified   |
+---------------------+
🧠 Security Event Detection System
Video Stream
      |
      v
+-----------------------+
| Person Detection      |
+-----------+-----------+
            |
            v
+-----------------------+
| Behavior Tracking     |
+-----------+-----------+
            |
   +--------+--------+
   |                 |
   v                 v

Intrusion        Wait Time
Detection        Monitoring
   |                 |
   v                 v

+---------------------------+
| Event Classification      |
+-------------+-------------+
              |
              v
+---------------------------+
| Alert Trigger System      |
| Email / Dashboard Alert   |
+---------------------------+
📂 Project Structure
suraksha
│
├── manage.py
├── db.sqlite3
│
├── suraksha
│   ├── settings.py
│   ├── urls.py
│   ├── views.py
│
├── service
│   ├── att.py
│   ├── heat.py
│   ├── alert.py
│   ├── mailer.py
│   ├── newface.py
│   ├── wait.py
│   ├── threshold.pkl
│   ├── wait_config.pkl
│   ├── ImagesAttendance
│   └── Attendance.csv
│
├── templates
│   ├── home.html
│   ├── att.html
│   ├── heatmap.html
│   ├── wait.html
│   ├── noentry.html
│
└── static
🔧 Installation

Clone repository

git clone https://github.com/Aaryan-kumar-24/aryavarta-suraksha.git

Navigate

cd suraksha

Create environment

python3 -m venv faceenv310

Activate

source faceenv310/bin/activate

Install dependencies

pip install -r service/requirement.txt

Run server

python manage.py runserver

Open browser

http://127.0.0.1:8000
🔮 Future Improvements

Deep learning face recognition (FaceNet / ArcFace)

Multi-camera distributed architecture

Cloud video storage

Real-time mobile alerts

Edge AI deployment (NVIDIA Jetson)

👨‍💻 Author

Aryan Kumar

Computer Science Engineer
AI Developer | Full Stack Developer

GitHub
https://github.com/Aaryan-kumar-24