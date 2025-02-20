from flask import Flask, render_template, request, redirect, url_for, session
import random
import sqlite3
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Function to initialize or connect to the SQLite database
def init_db():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS rolls (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        num_dice INTEGER,
        result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    conn.commit()
    conn.close()

init_db()

# Function to clear the roll history in the database
def clear_db():
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM rolls")
    conn.commit()
    conn.close()

# Roll the dice and store the result in the database
def roll_dice(num_dice):
    dice_rolls = [random.randint(1, 6) for _ in range(num_dice)]
    result = ', '.join(map(str, dice_rolls))

    # Store the roll in the database
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO rolls (num_dice, result) VALUES (?, ?)", (num_dice, result))
    conn.commit()
    conn.close()

    return dice_rolls, result

# Route to the homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    # If form is submitted, store the selected number of dice in session
    if request.method == 'POST':
        num_dice = request.form['num_dice']
        session['num_dice'] = num_dice  # Store selected dice in session

    # Get the last selected number of dice from session (default to 1 if not set)
    num_dice = session.get('num_dice', '1')

    # Get all the roll history
    conn = sqlite3.connect('game.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rolls ORDER BY timestamp DESC")
    history = cursor.fetchall()
    conn.close()

    return render_template('index.html', history=history, num_dice=num_dice)

# Route to roll the dice
@app.route('/roll', methods=['POST'])
def roll():
    num_dice = int(request.form['num_dice'])

    # Roll the dice and get the result
    dice_rolls, result = roll_dice(num_dice)

    # Generate the images for the dice rolled
    dice_images = [f"static/dice/dice{roll}.png" for roll in dice_rolls]

    return render_template('result.html', dice_rolls=dice_rolls, dice_images=dice_images, result=result)

# Route to clear the database and reset the UI
@app.route('/clear')
def clear():
    # Clear the database
    clear_db()

    # Redirect back to the home page with an empty history
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)

