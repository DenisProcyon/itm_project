import pandas as pd

from mongo_orm import MongoORM

import os
from dotenv import load_dotenv

MONGO_IP = os.getenv("MONGO_IP")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

def main():
    mongo_client = MongoORM(
        db=MONGO_DB,
        user=MONGO_USERNAME,
        password=MONGO_PASSWORD,
        ip=MONGO_IP,
        port=MONGO_PORT
    )

    channels = mongo_client.get_all_collections()
    
    posts = mongo_client.get_collection_entries(collection="readovkanews")

    channel_posts_comments = {}
    for post in posts:
        channel_posts_comments[post["_id"]] = {
            "text": post["text"],
            "comments": pd.DataFrame(post["comments"])
        }

    for post, data in channel_posts_comments.items():
        print(f'For post with id: {post} and text: {data["text"][:10]}... {len(data["comments"])} comments saved')
    

if __name__ == "__main__":
    main()