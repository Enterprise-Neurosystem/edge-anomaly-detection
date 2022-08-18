# edge-anomaly-detection
open source code for the detection of anomalies in sensor data
This web app allows you to broadcast various sources of data in real time

## Team Members
1. Audrey Reznik
1. Cameron Garrison
1. Christina Xu
1. Cory Latschkowski
1. Eli Guidera
1. Trevor Royer
1. Troy Nelson

##Meeting Information
Meetings are held every Thursday, 9-10 MST

Contact Audrey Reznik (areznik@redhat.com) for questions/comments/contributions.


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
