# edge-anomaly-detection

open source code for the detection of anomalies in sensor data
This web app allows you to broadcast various sources of data in real time

## OpenShift Setup

You can view the default parameters for `bootstrap.sh` [here](scripts/bootstrap.sh).

```
scripts/bootstrap.sh
```

## Local Quickstart

Setup local development

The following section only needs to be **run once**

```
python3 -m venv venv

# activate your virtual env with the following
. venv/bin/activate

pip install -r src/requirements.txt
```

Run app locally

```
# reactivate your virtual env with the following
. venv/bin/activate

cd src

# python debug
python3 wsgi.py

# gunicorn
gunicorn wsgi:application -b 0.0.0.0:8080
```

## Team Members

1. Audrey Reznik
1. Cameron Garrison
1. Christina Xu
1. Cory Latschkowski
1. Eli Guidera
1. Trevor Royer
1. Troy Nelson

## Meeting Information

Meetings are held every Thursday, 9-10 MST

Contact Audrey Reznik (areznik@redhat.com) for questions/comments/contributions.
