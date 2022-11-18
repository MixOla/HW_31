from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

from users.validators import check_birthdate


class Location(models.Model):
    name = models.CharField(max_length=100, unique=True)
    lat = models.DecimalField(max_digits=8, decimal_places=6, null=True)
    lng = models.DecimalField(max_digits=8, decimal_places=6, null=True)

    class Meta:
        verbose_name = "Местоположение"
        verbose_name_plural = "Местоположения"

    def __str__(self):
        return self.name


class UserRoles:
    MEMBER = 'member'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    choices = ((MEMBER, 'Пользователь'),
               (ADMIN, 'Администратор'),
               (MODERATOR, 'Модератор'))


class User(AbstractUser):
    age = models.PositiveSmallIntegerField(null=True, blank=True)
    role = models.CharField(choices=UserRoles.choices, default=UserRoles.MEMBER, max_length=10)
    location = models.ManyToManyField(Location)
    birthdate = models.DateField(validators=[check_birthdate])
    email = models.EmailField(verbose_name="email address", blank=True,
                              validators=[RegexValidator(regex="@rambler.ru", inverse_match=True,
                                                         message="Регистрация с домена rambler запрещена")])

    def save(self, *args, **kwargs):
        # self.set_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
