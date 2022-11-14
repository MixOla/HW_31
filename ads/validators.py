from rest_framework import serializers


def not_published(value):
    if value:
        raise serializers.ValidationError("Значение поля is_published при создании объявления не может быть True")