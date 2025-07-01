from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3
from datetime import datetime
import json

app = Flask(__name__)
app.secret_key = 'coping_companion_secret_key'

# Database setup
def init_db():
    conn = sqlite3.connect('coping_companion.db', timeout=10)
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            mood_rating INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS coping_mechanisms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            mechanism TEXT NOT NULL,
            effectiveness_rating INTEGER NOT NULL,
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def dashboard():
    conn = sqlite3.connect('coping_companion.db', timeout=10)
    cursor = conn.cursor()
    
    # Get recent entries
    cursor.execute('SELECT * FROM journal_entries ORDER BY date DESC LIMIT 5')
    recent_entries = cursor.fetchall()
    
    # Get recent mechanisms
    cursor.execute('SELECT * FROM coping_mechanisms ORDER BY date DESC LIMIT 5')
    recent_mechanisms = cursor.fetchall()
    
    # Get stats
    cursor.execute('SELECT COUNT(*) FROM journal_entries')
    total_entries = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM coping_mechanisms')
    total_mechanisms = cursor.fetchone()[0]
    
    cursor.execute('SELECT AVG(mood_rating) FROM journal_entries')
    avg_mood = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT AVG(effectiveness_rating) FROM coping_mechanisms')
    avg_effectiveness = cursor.fetchone()[0] or 0
    
    conn.close()
    
    return render_template('dashboard.html', 
                         recent_entries=recent_entries,
                         recent_mechanisms=recent_mechanisms,
                         total_entries=total_entries,
                         total_mechanisms=total_mechanisms,
                         avg_mood=round(avg_mood, 1) if avg_mood else 0,
                         avg_effectiveness=round(avg_effectiveness, 1) if avg_effectiveness else 0)

@app.route('/journal')
def journal():
    conn = sqlite3.connect('coping_companion.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM journal_entries ORDER BY date DESC')
    entries = cursor.fetchall()
    conn.close()
    return render_template('journal.html', entries=entries)

@app.route('/coping-mechanisms')
def coping_mechanisms():
    conn = sqlite3.connect('coping_companion.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM coping_mechanisms ORDER BY date DESC')
    mechanisms = cursor.fetchall()
    conn.close()
    return render_template('coping_mechanisms.html', mechanisms=mechanisms)

@app.route('/add_entry', methods=['POST'])
def add_entry():
    date = request.form['date']
    mood_rating = request.form['mood_rating']
    content = request.form['content']
    # Clear undo stack and counter for journal entries
    session['deleted_entry'] = []
    session['undo_entry_count'] = 0
    conn = sqlite3.connect('coping_companion.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO journal_entries (date, mood_rating, content) VALUES (?, ?, ?)',
                  (date, mood_rating, content))
    conn.commit()
    conn.close()
    
    return redirect(url_for('journal'))

@app.route('/delete_entry/<int:entry_id>', methods=['POST'])
def delete_entry(entry_id):
    conn = sqlite3.connect('coping_companion.db', timeout=10)
    cursor = conn.cursor()
    
    # Store the entry data before deleting for undo
    cursor.execute('SELECT * FROM journal_entries WHERE id = ?', (entry_id,))
    entry_data = cursor.fetchone()
    
    if entry_data:
        # Store in session for undo
        if 'deleted_entry' not in session:
            session['deleted_entry'] = []
        session['deleted_entry'].append({
            'date': entry_data[1],
            'mood_rating': entry_data[2],
            'content': entry_data[3]
        })
        # Increment undo counter
        session['undo_entry_count'] = session.get('undo_entry_count', 0) + 1
    
    cursor.execute('DELETE FROM journal_entries WHERE id = ?', (entry_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('journal'))

@app.route('/add_mechanism', methods=['POST'])
def add_mechanism():
    date = request.form['date']
    mechanism = request.form['mechanism']
    effectiveness_rating = request.form['effectiveness_rating']
    notes = request.form.get('notes', '')
    # Clear undo stack and counter for coping mechanisms
    session['deleted_mechanism'] = []
    session['undo_mechanism_count'] = 0
    conn = sqlite3.connect('coping_companion.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO coping_mechanisms (date, mechanism, effectiveness_rating, notes) VALUES (?, ?, ?, ?)',
                  (date, mechanism, effectiveness_rating, notes))
    conn.commit()
    conn.close()
    
    return redirect(url_for('coping_mechanisms'))

@app.route('/api/entries')
def api_entries():
    conn = sqlite3.connect('coping_companion.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM journal_entries ORDER BY date DESC')
    entries = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': entry[0],
        'date': entry[1],
        'mood_rating': entry[2],
        'content': entry[3]
    } for entry in entries])

@app.route('/api/mechanisms')
def api_mechanisms():
    conn = sqlite3.connect('coping_companion.db', timeout=10)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM coping_mechanisms ORDER BY date DESC')
    mechanisms = cursor.fetchall()
    conn.close()
    
    return jsonify([{
        'id': mechanism[0],
        'date': mechanism[1],
        'mechanism': mechanism[2],
        'effectiveness_rating': mechanism[3],
        'notes': mechanism[4]
    } for mechanism in mechanisms])

@app.route('/delete_mechanism/<int:mechanism_id>', methods=['POST'])
def delete_mechanism(mechanism_id):
    conn = sqlite3.connect('coping_companion.db', timeout=10)
    cursor = conn.cursor()
    
    # Store the mechanism data before deleting for undo
    cursor.execute('SELECT * FROM coping_mechanisms WHERE id = ?', (mechanism_id,))
    mechanism_data = cursor.fetchone()
    
    if mechanism_data:
        # Store in session for undo
        if 'deleted_mechanism' not in session:
            session['deleted_mechanism'] = []
        session['deleted_mechanism'].append({
            'date': mechanism_data[1],
            'mechanism': mechanism_data[2],
            'effectiveness_rating': mechanism_data[3],
            'notes': mechanism_data[4]
        })
        # Increment undo counter
        session['undo_mechanism_count'] = session.get('undo_mechanism_count', 0) + 1
    
    cursor.execute('DELETE FROM coping_mechanisms WHERE id = ?', (mechanism_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('coping_mechanisms'))

@app.route('/undo_entry', methods=['POST'])
def undo_entry():
    if 'deleted_entry' in session and session.get('undo_entry_count', 0) > 0:
        entry_data = session['deleted_entry'].pop()
        if entry_data:
            conn = sqlite3.connect('coping_companion.db', timeout=10)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO journal_entries (date, mood_rating, content) VALUES (?, ?, ?)',
                          (entry_data['date'], entry_data['mood_rating'], entry_data['content']))
            conn.commit()
            conn.close()
            # Decrement undo counter
            session['undo_entry_count'] = max(session.get('undo_entry_count', 1) - 1, 0)
    return redirect(url_for('journal'))

@app.route('/undo_mechanism', methods=['POST'])
def undo_mechanism():
    if 'deleted_mechanism' in session and session.get('undo_mechanism_count', 0) > 0:
        mechanism_data = session['deleted_mechanism'].pop()
        if mechanism_data:
            conn = sqlite3.connect('coping_companion.db', timeout=10)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO coping_mechanisms (date, mechanism, effectiveness_rating, notes) VALUES (?, ?, ?, ?)',
                          (mechanism_data['date'], mechanism_data['mechanism'], mechanism_data['effectiveness_rating'], mechanism_data['notes']))
            conn.commit()
            conn.close()
            # Decrement undo counter
            session['undo_mechanism_count'] = max(session.get('undo_mechanism_count', 1) - 1, 0)
    return redirect(url_for('coping_mechanisms'))

if __name__ == '__main__':
    app.run(debug=True, port=5001) 