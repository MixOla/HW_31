from django.db import models

from users.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Ad(models.Model):
    name = models.CharField(max_length=150, unique=True)
    author = models.ForeignKey(User, verbose_name="Автор", related_name='ads', on_delete=models.CASCADE)
    price = models.PositiveIntegerField()
    description = models.CharField(max_length=1000)
    is_published = models.BooleanField(default=True)
    image = models.ImageField(upload_to='media', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Обьявление"
        verbose_name_plural = "Обьявления"

    def __str__(self):
        return self.name