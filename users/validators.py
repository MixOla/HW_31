from datetime import date

from dateutil.relativedelta import relativedelta
from rest_framework.exceptions import ValidationError


def check_birthdate(birthdate):
    diff = relativedelta(date.today(), birthdate).years
    if diff < 9:
        raise ValidationError(f"Запрещена регистрация пользователям младше 9 лет.")