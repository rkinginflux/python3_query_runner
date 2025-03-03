# python3_query_runner
Web app written in Python to spin up a site to query your Influxdb3 databases.

Directory structure should look like this. 
```bash
<your directory>/
├── app.py
├── static
│   └── styles.css
└── templates
    └── index.html


Once your files are updated, run the following command to start up the service. 

uvicorn app:app --reload --host 0.0.0.0 --port 8000
