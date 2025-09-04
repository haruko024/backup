import os
import io
import bcrypt
import datetime
import random
import smtplib
import secrets
import socket
from email.mime.text import MIMEText
from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
import mysql.connector
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
MAX_CONTENT_LENGTH = 50 * 1024 * 1024 

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASS = os.getenv("SMTP_PASS")

def get_server_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        autocommit=True
    )

def get_db_connection():
    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        autocommit=True
    )

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # connect to Google DNS just to detect IP
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def init_db():
    server_conn = get_server_connection()
    cur = server_conn.cursor()
    cur.execute(
        f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"
    )
    cur.close()
    server_conn.close()

    conn = get_db_connection()
    cur = conn.cursor()

    # Users table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) UNIQUE NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        password_hash VARBINARY(255) NOT NULL,
        verified TINYINT(1) DEFAULT 0,
        qr_secret VARCHAR(512),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # Files table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS files (
        id INT AUTO_INCREMENT PRIMARY KEY,
        user_id INT NOT NULL,
        filename VARCHAR(512) NOT NULL,
        mime_type VARCHAR(255) NOT NULL,
        data LONGBLOB NOT NULL,
        size BIGINT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # OTP table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS otps (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(255) NOT NULL,
        otp_code VARCHAR(10) NOT NULL,
        expires_at DATETIME NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    conn.commit()
    cur.close()
    conn.close()

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

def verify_password(password: str, hashed: bytes) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(to_email, otp):
    subject = "Your OTP Code"

    # HTML email template with background
    html = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #4facfe, #00f2fe);
            margin: 0;
            padding: 0;
          }}
          .container {{
            background: #ffffff;
            max-width: 500px;
            margin: 40px auto;
            padding: 30px;
            border-radius: 12px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            text-align: center;
          }}
          h1 {{
            color: #2c3e50;
          }}
          .otp {{
            font-size: 28px;
            font-weight: bold;
            color: #3498db;
            margin: 20px 0;
            letter-spacing: 3px;
          }}
          p {{
            font-size: 16px;
            color: #555;
          }}
          .footer {{
            margin-top: 30px;
            font-size: 12px;
            color: #888;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h1>🔐 Secure File Management</h1>
          <p>Your One-Time Password (OTP) is:</p>
          <div class="otp">{otp}</div>
          <p>This code will expire in <b>5 minutes</b>.</p>
          <div class="footer">
            © 2025 Paul Mendoza — Secure File Management System
          </div>
        </div>
      </body>
    </html>
    """

    # Create MIME message
    msg = MIMEMultipart("alternative")
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject

    # Attach plain text fallback + HTML version
    text = f"Your OTP code is: {otp}\nIt will expire in 5 minutes."
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))

    # Send via SMTP
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
    server.starttls()
    server.login(SMTP_USER, SMTP_PASS)
    server.sendmail(SMTP_USER, to_email, msg.as_string())
    server.quit()

# def send_otp_email(to_email, otp):
#     subject = "Your OTP Code"
#     body = f"Your OTP code is: {otp}\nIt will expire in 5 minutes."
#     msg = MIMEText(body)
#     msg["From"] = SMTP_USER
#     msg["To"] = to_email
#     msg["Subject"] = subject

#     server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
#     server.starttls()
#     server.login(SMTP_USER, SMTP_PASS)
#     server.sendmail(SMTP_USER, to_email, msg.as_string())
#     server.quit()
    
local_ip = get_local_ip()
print(f"🔍 Detected local IP: {local_ip}")
app = Flask(__name__, template_folder="templates", static_folder="static")
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH
CORS(app, origins=[
    "http://localhost:5000",
    "http://127.0.0.1:5000",
    f"http://{local_ip}:5000"
    ])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/register", methods=["POST"])
def api_register():
    data = request.json
    username = data.get("username", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"ok": False, "error": "all fields required"}), 400

    hashed = hash_password(password)
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)",
            (username, email, hashed)
        )

        otp = generate_otp()
        expires_at = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        cur.execute(
            "INSERT INTO otps (username, otp_code, expires_at) VALUES (%s, %s, %s)",
            (username, otp, expires_at)
        )

        send_otp_email(email, otp)
        return jsonify({"ok": True, "msg": "OTP sent to your email"}), 201
    except mysql.connector.IntegrityError:
        return jsonify({"ok": False, "error": "username or email already exists"}), 409
    finally:
        cur.close()
        conn.close()

@app.route("/api/verify-otp", methods=["POST"])
def api_verify_otp():
    data = request.json
    username = data.get("username")
    otp_entered = data.get("otp")

    conn = get_db_connection()
    cur = conn.cursor(dictionary=True)
    cur.execute(
        "SELECT otp_code, expires_at FROM otps WHERE username=%s ORDER BY created_at DESC LIMIT 1",
        (username,)
    )
    row = cur.fetchone()
    if not row:
        return jsonify({"ok": False, "error": "no otp found"}), 400
    if row["otp_code"] != otp_entered:
        return jsonify({"ok": False, "error": "invalid otp"}), 400
    if datetime.datetime.utcnow() > row["expires_at"]:
        return jsonify({"ok": False, "error": "otp expired"}), 400

    qr_secret = secrets.token_urlsafe(32)
    cur.execute("UPDATE users SET verified=1, qr_secret=%s WHERE username=%s", (qr_secret, username))
    cur.execute("DELETE FROM otps WHERE username=%s", (username,))
    cur.close()
    conn.close()
    return jsonify({"ok": True, "qr_secret": qr_secret})

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.json
    username = data.get("username", "").strip()
    password = data.get("password", "")

    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash, verified, qr_secret FROM users WHERE username=%s", (username,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"ok": False, "error": "invalid credentials"}), 401
    user_id, password_hash, verified, qr_secret = row
    if not verified:
        return jsonify({"ok": False, "error": "email not verified"}), 403
    if verify_password(password, password_hash):
        return jsonify({"ok": True, "user_id": user_id, "username": username, "qr_secret": qr_secret}), 200
    return jsonify({"ok": False, "error": "invalid credentials"}), 401

@app.route("/api/login-qr", methods=["POST"])
def api_login_qr():
    data = request.json
    qr_secret = data.get("qr_secret")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, username, qr_secret FROM users WHERE qr_secret=%s AND verified=1", (qr_secret,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row:
        return jsonify({"ok": True, "user_id": row[0], "username": row[1], "qr_secret": row[2]})
    return jsonify({"ok": False, "error": "invalid qr"}), 401

@app.route("/api/upload", methods=["POST"])
def api_upload():
    if "file" not in request.files:
        return jsonify({"ok": False, "error": "file not provided"}), 400
    file = request.files["file"]
    user_id = request.form.get("user_id")
    data = file.read()
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO files (user_id, filename, mime_type, data, size) VALUES (%s, %s, %s, %s, %s)",
        (int(user_id), file.filename, file.mimetype or "application/octet-stream", data, len(data))
    )
    file_id = cur.lastrowid
    cur.close()
    conn.close()
    return jsonify({"ok": True, "file_id": file_id}), 201

@app.route("/api/list", methods=["GET"])
def api_list():
    user_id = request.args.get("user_id")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, filename, mime_type, size, created_at FROM files WHERE user_id=%s ORDER BY created_at DESC", (int(user_id),))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    files = [{"id": r[0], "filename": r[1], "mime_type": r[2], "size": r[3], "created_at": r[4].isoformat()} for r in rows]
    return jsonify({"ok": True, "files": files})

@app.route("/api/download/<int:file_id>", methods=["GET"])
def api_download(file_id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT filename, mime_type, data FROM files WHERE id=%s", (file_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if not row:
        return jsonify({"ok": False, "error": "file not found"}), 404
    filename, mime_type, data = row
    return send_file(io.BytesIO(data), mimetype=mime_type or "application/octet-stream", as_attachment=True, download_name=filename)

if __name__ == "__main__":
    init_db()
    app.run(host=os.getenv("FLASK_HOST"), port=int(os.getenv("FLASK_PORT")), debug=True)
