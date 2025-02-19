from core.models import User, Follow

users = [
        User(api_key="api1", name="Алексей"),
        User(api_key="api1", name="Михаил"),
        User(api_key="api1", name="Алина"),
    ]

follows = [
    Follow(follower_id=1, following_id=2),
    Follow(follower_id=2, following_id=1),
    Follow(follower_id=3, following_id=1),
]
