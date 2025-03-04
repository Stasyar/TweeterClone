from httpx import AsyncClient

from tests.good_response import (
    create_tweet,
    get_result,
    get_tweets,
    get_tweets_after_delete,
    get_tweets_after_like,
    get_tweets_after_unlike,
)


async def test_get_all_tweets(ac: AsyncClient):
    """Проверяем данные при запросе всех твитов в ленте."""
    response = await ac.get("/api/tweets", headers={"api-key": "test_1"})
    tweet_data = response.json()
    assert response.status_code == 200
    assert tweet_data == get_tweets


async def test_create_tweet(ac: AsyncClient):
    """Проверяем как добавляется твит."""
    payload = {"tweet_data": "Текст твита 3", "tweet_media_ids": []}
    response = await ac.post(
        "/api/tweets", json=payload, headers={"api-key": "test_1"}
    )
    response_data = response.json()
    assert response.status_code == 201
    assert response_data == create_tweet


async def test_delete_tweet(ac: AsyncClient):
    """Проверяем как удаляется твит."""
    response = await ac.delete("/api/tweets/2", headers={"api-key": "test_2"})
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == get_result

    response = await ac.get("/api/tweets", headers={"api-key": "test_2"})
    tweet_data = response.json()
    assert response.status_code == 200
    assert tweet_data == get_tweets_after_delete


async def test_like(ac: AsyncClient):
    """Проверяем как добавляется лайк."""
    response = await ac.post(
        "/api/tweets/1/likes", headers={"api-key": "test_3"}
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == get_result

    response = await ac.get("/api/tweets", headers={"api-key": "test_1"})
    tweet_data = response.json()
    assert response.status_code == 200
    assert tweet_data == get_tweets_after_like


async def test_unlike(ac: AsyncClient):
    """Проверяем как удаляется лайк."""
    response = await ac.delete(
        "/api/tweets/1/likes", headers={"api-key": "test_2"}
    )
    response_data = response.json()
    assert response.status_code == 200
    assert response_data == get_result

    response = await ac.get("/api/tweets", headers={"api-key": "test_1"})
    tweet_data = response.json()
    assert response.status_code == 200
    assert tweet_data == get_tweets_after_unlike
