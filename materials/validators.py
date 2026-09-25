from urllib.parse import urlparse

from rest_framework.serializers import ValidationError

YOUTUBE_HOST = "youtube.com"


def validate_video_link(value):
    """Проверяет, что ссылка на видео ведёт на youtube.com.

    Ссылки на сторонние ресурсы (образовательные платформы, личные сайты
    и т.п.) в материалах не допускаются.
    """
    host = urlparse(value).hostname or ""

    if host != YOUTUBE_HOST and not host.endswith(f".{YOUTUBE_HOST}"):
        raise ValidationError(
            "Разрешены только ссылки на видео с youtube.com."
        )

    return value