import os  # Importing os module to handle file operations
from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify  # Importing Flask modules
from flask_mysqldb import MySQL  # Importing MySQL support for Flask
from datetime import datetime  # Importing datetime to generate unique timestamps for filenames

app = Flask(__name__)  # Initializing Flask application

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'  # MySQL host
app.config['MYSQL_USER'] = 'root'  # MySQL username
app.config['MYSQL_PASSWORD'] = '12345678'  # MySQL password
app.config['MYSQL_DB'] = 'yukesh'  # MySQL database name
mysql = MySQL(app)  # Initializing MySQL connection

# Folder to store uploaded videos
UPLOAD_FOLDER = 'Videos'  # Define folder to store videos
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Set upload folder path
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Create folder if it doesn't exist

# Home Page Route - Shows the loading effect (index.html)
@app.route('/')
def index():
    return render_template('index.html')  # Show index.html first (loading effect)

# Website Page Route - This is the main website page after loading
@app.route('/website')
def website():
    return render_template('website.html')  # Load website.html after the loading effect

# Login Page Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # If form is submitted
        username = request.form['username']  # Get username
        password = request.form['password']  # Get password

        cursor = mysql.connection.cursor()  # Create MySQL cursor
        cursor.execute("SELECT * FROM user WHERE username = %s AND password = %s", (username, password))  # Query DB
        user = cursor.fetchone()  # Fetch user data
        cursor.close()  # Close cursor

        if user:  # If user exists, redirect to dashboard
            return redirect(url_for('dashboard'))
        else:  # If invalid credentials
            return "Invalid Credentials", 401

    return render_template('login.html')  # Show login page

# Signup Page Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':  # If form is submitted
        username = request.form['username']  # Get username
        password = request.form['password']  # Get password

        cursor = mysql.connection.cursor()  # Create MySQL cursor
        cursor.execute("INSERT INTO user (username, password) VALUES (%s, %s)", (username, password))  # Insert user
        mysql.connection.commit()  # Commit transaction
        cursor.close()  # Close cursor

        return redirect(url_for('login'))  # Redirect to login page

    return render_template('signup.html')  # Show signup page

# Dashboard Page Route
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')  # Show dashboard

# Recorder Page Route
@app.route('/recorder')
def recorder():
    return render_template('recorder.html')  # Show recorder page

# Upload Video Route
@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:  # Check if video file is in request
        return "No video uploaded!", 400  # Return error

    video = request.files['video']  # Get video file
    if video.filename == '':  # Check if file is empty
        return "No selected file!", 400  # Return error

    # Generate a unique filename using timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")  # Create timestamp
    filename = f"{timestamp}.webm"  # Name file using timestamp
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Full file path
    video.save(filepath)  # Save file to server

    # Store filename in MySQL database
    cursor = mysql.connection.cursor()  # Create MySQL cursor
    cursor.execute("INSERT INTO videos (filename) VALUES (%s)", (filename,))  # Insert video filename
    mysql.connection.commit()  # Commit transaction
    cursor.close()  # Close cursor

    return jsonify({"message": "Recording saved!", "filename": filename})  # Return success response

# Fetch and Display Recordings Route
@app.route('/recordings')
def recordings():
    cursor = mysql.connection.cursor()  # Create MySQL cursor
    cursor.execute("SELECT filename FROM videos ORDER BY upload_time DESC")  # Fetch filenames sorted by upload time
    videos = cursor.fetchall()  # Fetch video filenames
    cursor.close()  # Close cursor
    return render_template('recordings.html', videos=videos)  # Show recordings page

# Download Video Route
@app.route('/download/<filename>')
def download_video(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Get file path
    return send_file(filepath, as_attachment=True)  # Send file as downloadable attachment

# Delete Video Route
@app.route('/delete/<filename>')
def delete_video(filename):
    # Delete video record from MySQL database
    cursor = mysql.connection.cursor()  # Create MySQL cursor
    cursor.execute("DELETE FROM videos WHERE filename = %s", (filename,))  # Delete record
    mysql.connection.commit()  # Commit transaction
    cursor.close()  # Close cursor

    # Delete the video file from server storage
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)  # Get file path
    if os.path.exists(filepath):  # Check if file exists
        os.remove(filepath)  # Delete file

    return redirect(url_for('recordings'))  # Redirect to recordings page

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True)  # Run Flask app in debug mode
