import os
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # Change if needed
app.config['MYSQL_PASSWORD'] = '12345678'  # Change if needed
app.config['MYSQL_DB'] = 'yukesh'
mysql = MySQL(app)

# Folder to store uploaded videos
UPLOAD_FOLDER = 'Videos'  # New folder inside the project
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Ensure folder exists

# Home Page
@app.route('/')
def home():
    return render_template('website.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials", 401

    return render_template('login.html')

# Signup Page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('login'))

    return render_template('signup.html')

# Dashboard Page
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# Recorder Page
@app.route('/recorder')
def recorder():
    return render_template('recorder.html')

# Upload Video Route
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return "No video uploaded!", 400

    video = request.files['video']
    if video.filename == '':
        return "No selected file!", 400

    # Generate a unique filename based on timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{timestamp}.webm"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    video.save(filepath)

    # Store filename in MySQL
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO videos (filename) VALUES (%s)", (filename,))
    mysql.connection.commit()
    cursor.close()

    # Return filename for automatic download
    return jsonify({"message": "Recording saved!", "filename": filename})

# Fetch and Display Recordings
@app.route('/recordings')
def recordings():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT filename FROM videos ORDER BY upload_time DESC")
    videos = cursor.fetchall()
    cursor.close()
    return render_template('recordings.html', videos=videos)

# Download Video Route
@app.route('/download/<filename>')
def download_video(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(filepath, as_attachment=True)

# Delete Video Route
@app.route('/delete/<filename>')
def delete_video(filename):
    # Delete from MySQL
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM videos WHERE filename = %s", (filename,))
    mysql.connection.commit()
    cursor.close()

    # Delete from server folder
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(filepath):
        os.remove(filepath)

    return redirect(url_for('recordings'))

if __name__ == '__main__':
    app.run(debug=True)
