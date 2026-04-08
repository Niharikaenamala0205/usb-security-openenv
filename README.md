# 🔐 USB Security RL Environment

## 📌 Description
This project simulates a Reinforcement Learning environment for USB intrusion detection.

## ⚙️ API Endpoints

- POST /reset → Reset environment
- POST /step → Take action
- GET /state → Current state

## 🚀 Actions
- Allow
- Alert
- Block

## 🧠 States
- Owner
- Unknown
- Suspicious

## 🐳 Run with Docker

docker build -t usb-env .
docker run -p 7860:7860 usb-env

## 🌐 Live Demo
(Add your HuggingFace URL here)
