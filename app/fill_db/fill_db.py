from sqlalchemy import insert

from core.models import Follow, Like, Media, Tweet, User

USER_ID = "user_id"

users_data = [
    {"api_key": "api1", "name": "Алина"},
    {"api_key": "api2", "name": "Евгения"},
    {"api_key": "api3", "name": "Олег"},
    {"api_key": "api4", "name": "Паша"},
]

tweet_data = [
    {
        "content": "Мой рыжий котик",
        "author_id": 1,
        "likes": [
            {"id": 2, "name": "Евгения"},
            {"id": 3, "name": "Олег"},
            {"id": 4, "name": "Паша"},
        ],
        "media": [1],
    },
    {
        "content": "Мой черный котик",
        "author_id": 2,
        "likes": [
            {"id": 1, "name": "Алина"},
            {"id": 3, "name": "Олег"},
            {"id": 4, "name": "Паша"},
        ],
        "media": [2],
    },
    {
        "content": "Мой белый котик",
        "author_id": 3,
        "likes": [
            {"id": 1, "name": "Алина"},
            {"id": 3, "name": "Олег"},
            {"id": 4, "name": "Паша"},
        ],
        "media": [3],
    },
    {
        "content": "У меня нет котика",
        "author_id": 4,
        "likes": [{"id": 1, "name": "Алина"}],
        "media": [],
    },
]

like_data = [
    {"user_id": 2, "tweet_id": 1},
    {"user_id": 3, "tweet_id": 1},
    {"user_id": 4, "tweet_id": 1},
    {"user_id": 4, "tweet_id": 2},
    {"user_id": 3, "tweet_id": 2},
    {"user_id": 1, "tweet_id": 2},
    {"user_id": 4, "tweet_id": 3},
    {"user_id": 3, "tweet_id": 3},
    {"user_id": 1, "tweet_id": 3},
    {"user_id": 1, "tweet_id": 4},
]

followed_data = [
    {"follower_id": 1, "following_id": 2},
    {"follower_id": 2, "following_id": 1},
    {"follower_id": 1, "following_id": 3},
    {"follower_id": 1, "following_id": 4},
    {"follower_id": 2, "following_id": 3},
    {"follower_id": 2, "following_id": 4},
    {"follower_id": 3, "following_id": 1},
    {"follower_id": 3, "following_id": 4},
]

image_data = [
    {"filename": "medias/red.jpg"},
    {"filename": "medias/black.jpg"},
    {"filename": "medias/white.jpg"},
]


async def insert_data(conn):
    await conn.execute(insert(Media), image_data)
    await conn.execute(insert(User), users_data)
    await conn.execute(insert(Tweet), tweet_data)
    await conn.execute(insert(Like), like_data)
    await conn.execute(insert(Follow), followed_data)
