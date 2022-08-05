# edge-anomaly-detection
open source code for the detection of anomalies in sensor data
This web app allows you to broadcast various sources of data in real time

## Quickstart

Setup local development
```
python3 -m venv venv
. venv/bin/activate

pip install -r requirements.txt
```

Run app locally
```
# devel
python3 wsgi.py

# gunicorn
gunicorn wsgi:application -b 0.0.0.0:8080
```
