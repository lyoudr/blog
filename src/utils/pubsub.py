from google.cloud import pubsub_v1
import json
from sqlalchemy.orm import Session

from src.models.follow import Follow
from src.models.database import get_db
from src.models.user import User

PUBLISHER = pubsub_v1.PublisherClient()
TOPIC_PATH = PUBLISHER.topic_path("ann-project-390401", "post")

SUBSCRIBER = pubsub_v1.SubscriberClient()
SUBSCRIPTION_PATH = SUBSCRIBER.subscription_path("ann-project-390401", "post")


def publish_new_post_event(post):
    message = {
        "user_id": post.user_id,
        "post_id": post.id,
        "title": post.title,
    }
    # Encode the message to bytes
    future = PUBLISHER.publish(TOPIC_PATH, json.dumps(message).encode("utf-8"))
    future.result()


def callback(message):
    print(f"Received message: {message.data}")

    # Parse the message
    data = json.loads(message.data.decode("utf-8"))
    user_id = data["user_id"]
    post_id = data["post_id"]
    title = data["title"]

    # Open a DB session manually
    db_gen = get_db()
    db: Session = next(db_gen)

    try:
        # Query followers of the user
        followers = (
            db.query(Follow.follower_id, User.name)
            .join(User, Follow.follower_id == User.id)
            .filter(Follow.user_id == user_id)
            .all()
        )

        print(f"Followers of user {user_id}: {followers}")

        message.ack()
    except Exception as e:
        print(f"Error processing message: {e}")
        message.nack()
    finally:
        db.close()


def listen_for_messages():
    streaming_pull_future = SUBSCRIBER.subscribe(SUBSCRIPTION_PATH, callback=callback)
    print(f"Listening for messages on {SUBSCRIPTION_PATH}...")

    try:
        streaming_pull_future.result()
    except KeyboardInterrupt:
        streaming_pull_future.cancel()
