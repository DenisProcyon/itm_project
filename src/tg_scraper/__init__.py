from telethon import TelegramClient
import asyncio

from datetime import datetime

from telegram.post import Post
from telegram.comment import Comment

def transform_to_ts(date: str):
    try:
        return datetime.strptime(date, "%d/%m/%Y").timestamp()
    except Exception as e:
        raise ValueError(f'Can not transform {date} to timestamp. Required format: 07/03/2025')

async def get_posts(session: TelegramClient, channel: str, start: str = None, end: str = None, target_strings: list = []) -> list[Post]:
    start_ts = transform_to_ts(start)
    end_ts = transform_to_ts(end)

    async with session as client:
        try:
            posts = []
            async for message in client.iter_messages(channel):
                if message.date.timestamp() > end_ts:
                    continue

                if message.date.timestamp() < start_ts:
                    return posts
                
                if target_strings and not any(word.lower() in message.text.lower() for word in target_strings):
                    continue
                
                posts.append(
                    Post(
                        message.id,
                        text=message.message,
                        author=message.sender_id,
                        posting_ts=message.date.timestamp(),
                        comments=[]
                    )
                )

                print(f'{len(posts)} posts were found', end="\r")
            
            return posts
        except Exception as e:
            print(f'Error gathering posts: {e}')

            return []

async def get_comments(session: TelegramClient, channel: str, post: int | str):
    async with session as client:
        try:
            post = await client.get_messages(channel, ids=post.id)

            if not post:
                print(f'No post {post.id}')
                return

            comments = await client.get_messages(post.sender_id, reply_to=post.id, limit=1000)

            return [Comment(comment.id, comment.message, comment.sender_id, comment.date.timestamp(), post) for comment in comments]
        
        except Exception as e:
            print(f"Error: {e}")
