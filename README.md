# GCP Ingest API

Use this code to create a data ingest API that receives HTTP request and post them to Pub/sub.


## Develop
Create a virtual env with the packages used in this code.
```
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Change it according to your needs, then test it locally with 
```
export FLASK_APP=app
flask --debug run
```


## Build & Deploy
1. Set your project id with gcloud
```
gcloud config set project <your-project-id>
```

2. Run Cloud Build to build & deploy the container to Cloud Run using your Topic ID
```
gcloud builds submit . --config cloudbuild.yaml --substitutions _TOPIC_ID=<YOUR_TOPIC_ID>
```

## Testing
1. Post a message to the API URL
```
curl -X POST -d "test1" https://<your cloud run url> 
```

2. Go to Pub/sub, subscriptions, and pull the messages from your Topic's subscriptions

