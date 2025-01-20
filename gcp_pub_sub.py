from google.cloud import storage
from google.cloud import pubsub_v1
import json
from google.oauth2 import service_account
import threading

# Set your Google Cloud project ID and bucket name
topic_name = "test-5-pub-sub"
project_id = "able-stock-428615-n4"
bucket_name = "test-5-for-pub-sub"


credentials = service_account.Credentials.from_service_account_info(json.loads(credentials_json))

# Initialize clients with service account credentials
storage_client = storage.Client(credentials=credentials)
publisher = pubsub_v1.PublisherClient(credentials=credentials)
subscriber = pubsub_v1.SubscriberClient(credentials=credentials)

def create_bucket_if_not_exists(bucket_name):
    if not storage_client.lookup_bucket(bucket_name):
        bucket = storage_client.create_bucket(bucket_name)
        print(f"Bucket {bucket.name} created.")
    else:
        print(f"Bucket {bucket_name} already exists.")

def create_topic_if_not_exists(project_id, topic_name):
    topic_path = publisher.topic_path(project_id, topic_name)
    try:
        publisher.create_topic(request={"name": topic_path})
        print(f"Topic created: {topic_path}")
    except Exception as e:
        print(f"Topic {topic_path} already exists or error: {e}")

from google.cloud import storage


def create_bucket_notifications(bucket_name, topic_name):
    """Creates a notification configuration for a bucket."""
    # The ID of your GCS bucket
    # bucket_name = "your-bucket-name"
    # The name of a topic
    # topic_name = "your-topic-name"

    bucket = storage_client.bucket(bucket_name)
    notification = bucket.notification(topic_name=topic_name)
    notification.create()

    print(f"Successfully created notification with ID {notification.notification_id} for bucket {bucket_name}")

def upload_file(bucket_name, source_file_name, destination_blob_name):
    """Upload a file to the bucket."""
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    print(f"File {source_file_name} uploaded to {destination_blob_name}.")

def subscribe_to_topic(project_id, subscription_name, topic_name):
    subscription_path = subscriber.subscription_path(project_id, subscription_name)
    # publisher creates and send message to the topic
    topic_path = publisher.topic_path(project_id, topic_name)

    try:
        subscriber.create_subscription(request={"name": subscription_path, "topic": topic_path})
        print(f"Subscription created: {subscription_path}")
    except Exception as e:
        print(f"Subscription {subscription_path} already exists or error: {e}")

    def callback(message):
        print(f"Received message: {message}")
        
        message.ack()

    streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
    print(f"Listening for messages on {subscription_path}")

    try:
        streaming_pull_future.result()
    except Exception as e:
        print(f"Error during subscription: {e}")
        streaming_pull_future.cancel()

if __name__ == "__main__":
    create_bucket_if_not_exists(bucket_name)
    create_topic_if_not_exists(project_id, topic_name)
    create_bucket_notifications(bucket_name, topic_name, )

    thread = threading.Thread(
        target=subscribe_to_topic,
        args=(project_id, "test-5-subscription", topic_name),
        daemon=False
    )
    thread.start()
    
    # Upload a file to trigger the event
    upload_file(bucket_name, "test-file.txt", "uploaded_file.txt")

    try:
        while thread.is_alive():
            thread.join(1)
    except KeyboardInterrupt:
        print("Exiting...")

