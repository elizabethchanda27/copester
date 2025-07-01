#!/usr/bin/env python3
"""
Simple startup script for Coping Companion
"""
from app import app

if __name__ == '__main__':
    print("🧠 Starting Coping Companion...")
    print("📱 Open your browser and go to: http://localhost:5001")
    print("🛑 Press Ctrl+C to stop the server")
    app.run(debug=True, port=5001, host='0.0.0.0') 