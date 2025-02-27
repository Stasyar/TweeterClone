from pathlib import Path

from httpx import AsyncClient

from tests.good_response import image_load


async def test_image_load(ac: AsyncClient):
    """Проверяем как загружается картинка."""
    test_img = Path("tests/image_for_test/image_for_testing.jpg")

    with test_img.open("rb") as img_file:
        response = await ac.post(
            "/api/medias",
            files={"file": ("image_for_testing.jpg", img_file, "image/jpeg")},
        )

    img_data = response.json()
    assert response.status_code == 200
    assert img_data == image_load
