import http
import os
import logging
from wsgiref import validate
from flask import Flask, request
from google.cloud import pubsub_v1

app = Flask(__name__)


@app.route("/", methods=['POST'])
def publish():
    try:
        # Request validation
        # TO-DO - If you need to validate the request, add your code here

        # read env vars
        project_id = read_env_var("PROJECT_ID")
        topic_id = read_env_var("TOPIC_ID")
        source_system = read_env_var("SOURCE_SYSTEM")

        # Pub/sub publisher
        publisher = pubsub_v1.PublisherClient()
        topic_path = publisher.topic_path(project_id, topic_id)
        logging.info("Topic path {}".format(topic_path))

        # Get the request data
        data = request.get_data()

        # message attributes
        msg_attrs = {
            "source_system": source_system,
            "image": "gcp-ingest-api"
        }

        # Publish the message to Pub/sub
        future = publisher.publish(topic_path, data, attrs=msg_attrs)
        logging.info(future.result())
    except Exception:
        return 'error', http.HTTPStatus.INTERNAL_SERVER_ERROR

    return 'success'


# Get env vars and log error if not found
def read_env_var(var_name):
    var_value = os.environ.get(var_name)
    if not var_value:
        logging.error("Missing env var {}={}".format(var_name, var_value))
    return var_value


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
