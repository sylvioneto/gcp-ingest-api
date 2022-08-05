import http
import os
import logging
from wsgiref import validate
from flask import Flask, request
from google.cloud import pubsub_v1

app = Flask(__name__)
app.config.from_pyfile('settings.py')


@app.route("/", methods=['POST'])
def publish():
    try:
        # Request validation
        # TO-DO - If you need to validate the request, add your code here

        # read env vars
        project_id = app.config.get("PROJECT_ID")
        topic_id = app.config.get("TOPIC_ID")
        source_system = app.config.get("SOURCE_SYSTEM")

        print(project_id)

        # Pub/sub publisher
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        logging.info("Topic path {}".format(topic_path))

        # Get the request data
        data = request.get_data()

        if not source_system:
            source_system = "unknown"

        # Publish the message to Pub/sub
        future = publisher.publish(topic_path, data, source_system=source_system, image="gcp-ingest-api")
        logging.info(future.result())
    except Exception as ex:
        logging.error(ex)
        return 'error:{}'.format(ex), http.HTTPStatus.INTERNAL_SERVER_ERROR

    return 'success'


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
