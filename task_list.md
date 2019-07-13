# Task list

* Make environment name a required argument for Honeycomb worker
* Add option of specifying environment ID rather than environment name
* Separate Honeycomb worker from main shoe sensor repo?
* Revise setup.py/requirements.txt/Dockerfile to include new dependencies:
    - database_connection
    - database_connection_honeycomb
    - honeycomb
    - gqlpycgen
* Add worker that sends data to Celery (thence to Honeycomb)
* Add worker to assign shoe sensors to environment?
* Add worker to configure shoe sensors?
* Combine workers (switch destination with command line option)?
* Move details of data fields, etc. to shared constants
