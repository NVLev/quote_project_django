import pytest
from django.contrib.auth.models import User
from quotes.models import Quote, Source

@pytest.fixture
def user():
    """Фикстура пользователя"""
    return User.objects.create_user(
        username='testuser',
        password='testpass123'
    )

@pytest.fixture
def source():
    """Фикстура источника"""
    return Source.objects.create(name="Test Source")

@pytest.fixture
def quote(source):
    """Фикстура цитаты"""
    return Quote.objects.create(
        text="Test Quote Text",
        source=source,
        likes=0,
        dislikes=0,
        view_count=0
    )