from core.models import User, Follow, Tweet, Like, Media

USER_ID = "user_id"

users_data = [
    {"api_key": "test_1"},
    {"api_key": "test_2"},
]

tweet_data = [
    {
        "content": "Text for test tweet 1",
        "author_id": 1,
        "media": [1]
    },
    {
        "content": "Текст для теста твита 2",
        "author_id": 2,
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

image_data = {"tweet_id": 1, "filename": "medias/image_for_test.jpg"}


async def insert_data(session):
    users = [User(api_key=u.get("api_key")) for u in users_data]
    tweets = [Tweet(content=t.get("content"), author_id=t.get("author_id")) for t in tweet_data]
    likes = [Like(user_id=l.get("user_id"), tweet_id=l.get("tweet_id")) for l in like_data]
    follows = [Follow(follower_id=f.get("follower_id"), following_id=f.get("following_id"))
               for f in followed_data]
    media = Media(filename=image_data.get("filename"))

    async with session() as async_session:
        async_session.add_all(users)
        await async_session.commit()

        async_session.add_all(tweets)
        await async_session.commit()

        async_session.add_all(likes)
        await async_session.commit()

        async_session.add_all(follows)
        await async_session.commit()

        async_session.add_all(media)
        await async_session.commit()





