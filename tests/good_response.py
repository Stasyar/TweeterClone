get_tweets = {
    "result": True,
    "tweets": [
        {
            "id": 2,
            "content": "Текст для теста твита 2",
            "attachments": [],
            "author": {"id": 2, "name": None},
            "likes": [{"user_id": 1, "name": None}],
        },
        {
            "id": 1,
            "content": "Текст для теста твита 1",
            "attachments": ["http://localhost/medias/image_for_test.jpg"],
            "author": {"id": 1, "name": None},
            "likes": [{"user_id": 2, "name": None}],
        },
    ],
}

get_tweets_after_delete = {
    "result": True,
    "tweets": [
        {
            "id": 1,
            "content": "Текст для теста твита 1",
            "attachments": ["http://localhost/medias/image_for_test.jpg"],
            "author": {"id": 1, "name": None},
            "likes": [{"user_id": 2, "name": None}],
        },
    ],
}

get_tweets_after_like = {
    "result": True,
    "tweets": [
        {
            "id": 1,
            "content": "Текст для теста твита 1",
            "attachments": ["http://localhost/medias/image_for_test.jpg"],
            "author": {"id": 1, "name": None},
            "likes": [
                {"user_id": 2, "name": None},
                {"user_id": 3, "name": None},
            ],
        },
        {
            "id": 2,
            "content": "Текст для теста твита 2",
            "attachments": [],
            "author": {"id": 2, "name": None},
            "likes": [{"user_id": 1, "name": None}],
        },
    ],
}

get_tweets_after_unlike = {
    "result": True,
    "tweets": [
        {
            "id": 2,
            "content": "Текст для теста твита 2",
            "attachments": [],
            "author": {"id": 2, "name": None},
            "likes": [{"user_id": 1, "name": None}],
        },
        {
            "id": 1,
            "content": "Текст для теста твита 1",
            "attachments": ["http://localhost/medias/image_for_test.jpg"],
            "author": {"id": 1, "name": None},
            "likes": [],
        },
    ],
}

get_user = {
    "result": True,
    "user": {
        "id": 1,
        "name": None,
        "followers": [{"id": 2, "name": None}],
        "following": [{"id": 2, "name": None}],
    },
}

get_user_after_follow_test = {
    "result": True,
    "user": {
        "id": 1,
        "name": None,
        "followers": [{"id": 2, "name": None}, {"id": 3, "name": None}],
        "following": [{"id": 2, "name": None}],
    },
}

get_user_after_unfollow_test = {
    "result": True,
    "user": {
        "id": 1,
        "name": None,
        "followers": None,
        "following": [{"id": 2, "name": None}],
    },
}


get_result = {"result": True}

create_tweet = {"result": True, "tweet_id": 3}

image_load = {"result": True, "media_id": 2}
