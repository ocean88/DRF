import re
from rest_framework.serializers import ValidationError


class TitleValidator:
    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        reg = re.compile("^[А-Яа-яA-Za-z0-9]+$")
        tmp_val = value.get(self.field)
        if not bool(reg.fullmatch(tmp_val)):
            raise ValidationError(f"Неверное значение в поле {self.field}: {tmp_val}")


def validate_video_url(value):
    if not isinstance(value, str):
        raise ValidationError("Некорректный тип данных, ожидается строка")

    youtube_regex = re.compile(
        r"^(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/.+$"
    )

    if not youtube_regex.match(value):
        raise ValidationError("Видео должно быть с YouTube")
