get_tweets = {
    "tweets": [
        {
            "user_id": 2,
            "content": "Текст для теста твита 2",
            "author": {"user_id": 2, "name": None},
            "likes": [{"user_id": 1, "name": None}],
            "attachments": [],
        },
        {
            "user_id": 1,
            "content": "Text for test tweet 1",
            "author": {"user_id": 1, "name": None},
            "likes": [{"user_id": 2, "name": None}],
            "attachments": ["images/image_for_test.jpg"],
        },
    ]
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

get_result = {"result": True}

create_tweet = {"result": True, "tweet_id": 3}

image_load = {"result": True, "media_id": 2}
