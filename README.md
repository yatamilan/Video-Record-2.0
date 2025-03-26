# Video Recorder Project

## 📌 Overview  
The **Video Recorder Project** is a web-based application that allows users to record their screen, preview recordings, and download them. It includes a **user authentication system** with login and signup functionality.  

## 🚀 Features  

### 🔹 Frontend Features  
✅ **Welcome Page (`index.html`)**  
- Animated text and background effect  
- Auto-redirects to `website.html` after 3 seconds  

✅ **Main Website (`website.html`)**  
- Hero section with welcome text  
- Features list (Screen Recording, Download, Preview)  
- Login & Signup buttons  

✅ **Login Page (`login.html`)**  
- Accepts **username & password** input  
- Sends login data to the backend (`server.py`)  
- Redirects to `dashboard.html` on successful login  

✅ **Signup Page (`signup.html`)**  
- Allows **new user registration**  
- Stores user credentials in `users.txt`  

✅ **Dashboard (`dashboard.html`)**  
- Displays **Welcome Message**  
- "Start Recording" button (Links to `recorder.html`)  

✅ **Screen Recorder (`recorder.html`)**  
- Uses **MediaRecorder API** for screen recording  
- Allows **preview & download** of the recording  

✅ **Recordings Page (`recordings.html`)**  
- Displays **previously recorded videos** stored in **localStorage**  
- Users can **delete recordings**  

---

## 🛠️ Tech Stack  
- **Backend:** Python (Flask)  
- **Frontend:** HTML, Tailwind CSS, JavaScript  
- **Storage:** `users.txt` for login credentials  
- **Screen Recording:** MediaRecorder API  

---

## 📂 Project Structure  
/video_recorder_project 
│── /templates 
│ ├── index.html
│ ├── website.html 
│ ├── login.html 
│ ├── signup.html 
│ ├── dashboard.html 
│ ├── recorder.html 
│ ├── recordings.html 
│── /static 
│ ├── styles.css (if needed) 
│── server.py 
│── README.md


---

## 🎯 How to Run  

### 🔹 Step 1: Install Flask  
If Flask is not installed, install it using:  
```bash
pip install flask

### Step 2: Run the Server
Navigate to the project folder and execute:
```bash
python server.py

### Step 3: Open in Browser
Go to: http://127.0.0.1:5000/

## 📬 Contact
📩 Email: yukeshstark13@gmail.com
📷 Instagram: @mr.yukeshwaran
