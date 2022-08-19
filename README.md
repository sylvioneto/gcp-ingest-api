# GCP Ingest API

Use this code to create a data ingest API that receives HTTP request and post them to Pub/sub.
You can use the parameter `entity` to route your messages on Pub/sub.


## Develop
Create a virtual env with the packages used in this code.
```
python3 -m virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

Change it according to your needs, then test it locally with 
```
export FLASK_APP=main.py
flask --debug run
```
Post a message
```
curl http://127.0.0.1:5000?entity=person -d "John" 
```


## Build & Deploy
1. Set your project id with gcloud
```
gcloud config set project <your-project-id>
```

2. Create a Artifact Registry for Docker
```
gcloud artifacts repositories create docker-repo \
    --repository-format=docker \
    --location=us-central1 \
    --description="Private docker images"
```

3. Run Cloud Build to build & publish the container to the Artifact Registry
```
gcloud builds submit . --config cloudbuild.yaml
```

## Testing
1. Deploy the image to Cloud Run as a service informing the TOPIC_ID and PROJECT_ID where the data ingested should be storage.

2. Post a message to the Service's URL, for example
```
curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" \
    -d "{"order_id": "1awq2"}" \
    https://<your-cloud-run-url>/?entity=order-event
```

3. Go to [Pub/sub, subscriptions](https://console.cloud.google.com/cloudpubsub/subscription), click on the subscription, click on PULL and check the messages.


## Known issues
- Access Denied: Grant Cloud Run Invoker to your user and/or service account
- Unauthenticated when running `curl`: authenticate gcloud with `gcloud auth application-default login`
