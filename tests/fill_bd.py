from sqlalchemy import insert

from core.models import Follow, Like, Media, Tweet, User

users_data = [
    {"api_key": "test_1"},
    {"api_key": "test_2"},
]

tweet_data = [
    {
        "content": "Текст для теста твита 1",
        "author_id": 1,
        "likes": [{"id": 2, "name": None}],
        "media": [1],
    },
    {
        "content": "Текст для теста твита 2",
        "author_id": 2,
        "likes": [{"id": 1, "name": None}],
        "media": [],
    },
]

like_data = [
    {"user_id": 1, "tweet_id": 2},
    {"user_id": 2, "tweet_id": 1},
]

followed_data = [
    {"follower_id": 1, "following_id": 2},
    {"follower_id": 2, "following_id": 1},
]

image_data = {"filename": "medias/image_for_test.jpg"}


async def insert_data(conn):
    await conn.execute(insert(Media), image_data)
    await conn.execute(insert(User), users_data)
    await conn.execute(insert(Tweet), tweet_data)
    await conn.execute(insert(Like), like_data)
    await conn.execute(insert(Follow), followed_data)
