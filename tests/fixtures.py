from datetime import date, timedelta

import pytest


@pytest.fixture
@pytest.mark.django_db
def access_token(client, django_user_model):
    username = "test_user"
    password = "testpass"
    birthdate = date.today() - timedelta(days=5000)

    django_user_model.objects.create_user(username=username, password=password,
                                          birthdate=birthdate, role="admin")
    response = client.post("/user/token/", {"username": username, "password": password},
                           content_type="application/json")

    return response.data['access']
