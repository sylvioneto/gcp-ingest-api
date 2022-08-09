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

        PROJECT_ID = app.config.get("PROJECT_ID")
        TOPIC_ID = app.config.get("TOPIC_ID")
        SOURCE_SYSTEM = app.config.get("SOURCE_SYSTEM")

        # Pub/sub publisher
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(PROJECT_ID, TOPIC_ID)
        logging.info("Topic path {}".format(topic_path))

        # Get the request data
        data = request.get_data()

        if not SOURCE_SYSTEM:
            SOURCE_SYSTEM = "unknown"

        # Publish the message to Pub/sub
        future = publisher.publish(
            topic_path, data, source_system=SOURCE_SYSTEM, image="gcp-ingest-api")
        logging.info(future.result())
    except Exception as ex:
        logging.error(ex)
        return 'error:{}'.format(ex), http.HTTPStatus.INTERNAL_SERVER_ERROR

    return 'success'


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
