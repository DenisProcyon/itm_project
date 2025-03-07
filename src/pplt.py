from telethon import TelegramClient
import asyncio

from tg_scraper import get_comments, get_posts

import os
from dotenv import load_dotenv

from  mongo_orm import MongoORM
from telegram.post import Post
from telegram.comment import Comment

load_dotenv()

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")

MONGO_IP = os.getenv("MONGO_IP")
MONGO_PORT = os.getenv("MONGO_PORT")
MONGO_DB = os.getenv("MONGO_DB")
MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")

CHANNEL_USERNAME = '@RVvoenkor'
TARGET_STRINGS = ["укр"]
START = "03/03/2025"
END = "04/03/2025"

async def save_to_mongo(mongo_client: MongoORM, posts: list[Post]):
    mongo_client.save_new_channel_posts(channel=CHANNEL_USERNAME, posts=posts)

async def get_tg_posts() -> list[Post]:
    async with TelegramClient("session", API_ID, API_HASH) as session:
        posts = await get_posts(session, CHANNEL_USERNAME, start=START, end=END, target_strings=TARGET_STRINGS)
        
        for index, post in enumerate(posts):
            post.comments = await get_comments(session=session, channel=CHANNEL_USERNAME, post=post)

            print(f'Got comments for post {index + 1} out of {len(posts)}', end="\r")
        
        return posts

async def main():
    """
    Script to populate the database with data from given channel and given trigger strings. 
    Trigger strings are those which whould be seen in the text of the post.

    You can filter posts by date, start and end parameters
    """
    mongo_client = MongoORM(
        db=MONGO_DB,
        user=MONGO_USERNAME,
        password=MONGO_PASSWORD,
        ip=MONGO_IP,
        port=MONGO_PORT
    )

    posts = await get_tg_posts()

    await save_to_mongo(mongo_client=mongo_client, posts=posts)

if __name__ == "__main__":
    asyncio.run(main())
