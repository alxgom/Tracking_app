# ⏱ Tracking App

A modern, full-stack task tracking application built with **FastAPI** (Backend) and **React + Vite** (Frontend). Designed for simplicity, efficiency, and security.

## 🚀 Features

- **Dual Timer Modes**: Toggle between a standard **Stopwatch** (count up) and a **Countdown Timer** (count down).
- **Preset Focus Sessions**: Quick 25m (Pomodoro) and 50m presets, plus custom duration support.
- **Smart Notifications**: Browser notifications alert you when your timer finishes.
- **Advanced Analytics**:
  - **By Task**: Visualize total focus time per task.
  - **By Date**: Time-series view to track daily productivity trends.
  - **Aligned Layout**: Perfectly grid-aligned bars for clear visual comparison.
- **Robust Security**:
  - **Pydantic Validation**: Strict input schemas for tasks and logs.
  - **SQLi Protection**: Parameterized queries via SQLAlchemy ORM.
  - **Unit Tested**: Comprehensive test suite for backend logic.

## 🛠 Tech Stack

- **Backend**: Python 3.10+, FastAPI, SQLAlchemy, Pydantic, SQLite.
- **Frontend**: React, Vite, Vanilla CSS (Glassmorphism), HSL-based dynamic styling.
- **Testing**: Pytest, HTTpx.

## 🚦 Getting Started

### Backend Setup
1. Navigate to `/backend`.
2. Install dependencies: `pip install -r requirements.txt` (or use Poetry).
3. Run the server: `uvicorn main:app --reload`.

### Frontend Setup
1. Navigate to `/frontend`.
2. Install dependencies: `npm install`.
3. Start the dev server: `npm run dev`.

## 🧪 Running Tests
```bash
cd backend
pytest
```
