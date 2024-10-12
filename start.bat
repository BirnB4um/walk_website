@echo off

set FLASK_APP=app.py
set FLASK_DEBUG=1
set PORT=5000


if %FLASK_DEBUG%==1 (
    flask run --host=0.0.0.0 --port=%PORT%
) else (
    gunicorn -w 4 -b 0.0.0.0:%PORT% app:app
)
