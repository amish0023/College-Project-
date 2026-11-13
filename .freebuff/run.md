# Run Doc — Personalised Learning Flask App

## How to reproduce the server

The Flask app runs from the project root using Python.

### 1. Ensure MySQL is running (XAMPP)

The app connects to `localhost:3306`, database `personalised_learning`, user `root`, no password.

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Import the database schema (if not already done)

```bash
"C:\xampp\mysql\bin\mysql.exe" -u root < database.sql
```

### 4. Train the ML model (if `ml/model.pkl` is missing)

```bash
python ml/train_model.py
```

## How to start the server

### Foreground (for debugging)

```bash
python app.py
```

The app starts on `http://127.0.0.1:5000/`.

### Background (detached, for preview)

```bash
python -c "import subprocess; p = subprocess.Popen(['python', 'app.py'], stdout=open('.freebuff/preview-99f4a346-744d-4758-872f-47f1d248451f.log','w'), stderr=open('.freebuff/preview-99f4a346-744d-4758-872f-47f1d248451f.log.err','w')); print(f'PID={p.pid}')"
```

## Stopping the server

```bash
powershell -NoProfile -Command "Get-Process -Id <pid> | Stop-Process -Force"
```

## Current state

- **Port:** 5000
- **Last known PID:** 33948
- **Status:** Running and verified healthy
