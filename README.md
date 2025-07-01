# 🧠 Coping Companion

A simple mental health journaling and coping mechanism tracking app built with Python Flask.

## Features

- 📝 **Journal Entries**: Track your daily thoughts and mood
- 🎯 **Coping Mechanisms**: Monitor which strategies work best for you
- 📊 **Dashboard**: View your mental health overview and recent activity
- 💾 **Local Storage**: All data stored in SQLite database

## Quick Start

1. **Install Flask** (if not already installed):

   ```bash
   pip install Flask==2.3.3
   ```

2. **Run the app**:

   ```bash
   python run.py
   ```

3. **Open your browser** and go to:
   ```
   http://localhost:5001
   ```

## How to Use

### Dashboard

- View your overall stats and recent activity
- Quick access to add new entries or coping mechanisms

### Journal

- Add daily journal entries with mood ratings (1-10)
- Write about your thoughts, feelings, and experiences
- View all your past entries

### Coping Mechanisms

- Track which coping strategies you use
- Rate their effectiveness (1-10)
- Add notes about what worked or didn't work
- Get ideas for new coping strategies

## File Structure

```
copester-1/
├── app.py              # Main Flask application
├── run.py              # Startup script
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── journal.html
│   └── coping_mechanisms.html
└── coping_companion.db # SQLite database (created automatically)
```

## Data Storage

All your data is stored locally in a SQLite database file (`coping_companion.db`). This means:

- ✅ Your data stays private on your computer
- ✅ No internet connection required
- ✅ No account setup needed
- ⚠️ Data is stored locally - backup the database file if needed

## Stopping the App

Press `Ctrl+C` in the terminal where the app is running to stop the server.

---

**Note**: This is a simple local app for personal use. For professional mental health support, please consult with qualified healthcare providers.
