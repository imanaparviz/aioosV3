# 🚀 AIOOS Project Walkthrough

Welcome to the **AIOOS Voice AI Platform**! This guide will walk you through the project in small, digestible steps.

## 1. The Big Picture 🌍
This project is a **Voice AI Platform** that lets you create intelligent voice agents (like Siri or Alexa, but custom-made).
- **Goal:** Build agents that can listen, think (using AI), and speak back in real-time.
- **Key Tech:** It uses **LiveKit** for audio streaming, **OpenAI** for intelligence, and **Azure** for high-quality speech.

## 2. Project Structure 📂
The project is split into two main parts:

### 🧠 Backend (`v4liveKit/backend`)
This is the "brain" of the operation.
- **Language:** Python 🐍
- **Key File:** `main.py` (This is where the app starts)
- **Configuration:** `.env` file (Stores your API keys for OpenAI, Azure, etc.)
- **What it does:** Handles the logic, connects to AI services, and manages the voice processing.

### 🎨 Frontend (`v4liveKit-frontend`)
This is the "face" of the operation.
- **Language:** JavaScript/Vue.js ⚡
- **Framework:** Vite (for fast development)
- **What it does:** Provides a web interface to log in, manage agents, and test the voice chat.

## 3. Key Scripts (The "Magic Buttons") 🪄
In the root folder, you'll see some numbered `.bat` files. These are designed to make your life easy on Windows:

- **`1-INSTALL.bat`**: Runs the setup. It installs all the necessary libraries for both backend and frontend. **Run this once.**
- **`2-START.bat`**: Starts the whole system. It opens two terminal windows (one for backend, one for frontend) and launches your browser. **Use this daily.**
- **`3-STOP.bat`**: Shuts everything down cleanly.

## 4. How to Get Started (Step-by-Step) 👣

### Step 1: Install Dependencies
Double-click `1-INSTALL.bat`. It will take a few minutes to download everything.

### Step 2: Configure Secrets
You need to tell the app your API keys.
1. Go to `v4liveKit/backend`.
2. Open the `.env` file (created after installation).
3. Fill in your keys:
   - `LIVEKIT_URL`, `LIVEKIT_API_KEY`, `LIVEKIT_API_SECRET` (from LiveKit Cloud)
   - `OPENAI_API_KEY` (from OpenAI)
   - `AZURE_SPEECH_KEY` (from Azure)

### Step 3: Launch! 🚀
Double-click `2-START.bat`.
- Wait for the windows to say "Ready".
- Your browser should open to `http://localhost:5173`.

### Step 4: Test It
1. Log in (or sign up) on the web page.
2. Go to "Test Agent".
3. Click the microphone icon and say "Hello!".
4. The agent should reply!

## 5. Where to Look Next? 📖
- **`QUICK_START.md`**: A fast, "Finglish" guide if you prefer that style.
- **`README_WINDOWS.md`**: Detailed Windows-specific instructions.
- **`TROUBLESHOOTING.md`**: If something goes wrong, check here first.

---
**Ready to dive in?** Let me know if you want to zoom in on any specific part (like "How does the backend code work?" or "How do I change the voice?").
