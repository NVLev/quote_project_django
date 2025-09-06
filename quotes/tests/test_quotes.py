import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from quotes.forms import QuoteForm
from quotes.models import Quote, Source


@pytest.mark.django_db
def test_random_quote_view(client):
    source = Source.objects.create(name="Test Book")
    Quote.objects.create(text="Test quote", source=source, base_weight=5)

    response = client.get(reverse("quotes:random_quote"))
    assert response.status_code == 200
    assert b"Test quote" in response.content


@pytest.mark.django_db
def test_add_quote_limit(client):
    source = Source.objects.create(name="Book1")

    for i in range(3):
        Quote.objects.create(text=f"Quote {i}", source=source)

    form_data = {
        "text": "Quote 4",
        "source": source.id,
    }
    form = QuoteForm(data=form_data)

    print("Form errors:", form.errors)
    print("Form non-field errors:", form.non_field_errors())

    assert not form.is_valid()

    non_field_errors = form.non_field_errors()
    assert len(non_field_errors) > 0
    assert "лимит исчерпан" in str(non_field_errors[0]).lower()


@pytest.mark.django_db
def test_like_quote_authenticated(client, user, quote):
    """Тест лайка от авторизованного пользователя"""
    client.force_login(user)
    url = reverse("quotes:like_quote", args=[quote.id])

    response = client.post(url)

    quote.refresh_from_db()
    assert response.status_code == 302
    assert quote.likes == 1

    session_key = f"voted_quote_{quote.id}"
    assert session_key in client.session
    assert client.session[session_key] is True


@pytest.mark.django_db
def test_dislike_quote_authenticated(client, user, quote):
    """Тест дизлайка от авторизованного пользователя"""
    client.force_login(user)
    url = reverse("quotes:dislike_quote", args=[quote.id])

    response = client.post(url)

    quote.refresh_from_db()
    assert response.status_code == 302
    assert quote.dislikes == 1
    session_key = f"voted_quote_{quote.id}"
    assert session_key in client.session
    assert client.session[session_key] is True


@pytest.mark.django_db
def test_like_quote_anonymous(client, quote):
    """Тест что анонимный пользователь перенаправляется на логин"""
    url = reverse("quotes:like_quote", args=[quote.id])

    response = client.post(url)

    assert response.status_code == 302
    assert response.url.startswith("/users/login/")  # Перенаправление на логин
    quote.refresh_from_db()
    assert quote.likes == 0


@pytest.mark.django_db
def test_double_vote_prevention(client, user, quote):
    """Тест защиты от двойного голосования"""
    client.force_login(user)
    url_like = reverse("quotes:like_quote", args=[quote.id])

    client.post(url_like)
    quote.refresh_from_db()
    assert quote.likes == 1

    client.post(url_like)
    quote.refresh_from_db()
    assert quote.likes == 1


@pytest.mark.django_db
def test_top_quotes_view(client):
    """Тест страницы топа цитат"""
    source = Source.objects.create(name="Test Source")

    quote1 = Quote.objects.create(text="Quote 1", source=source, likes=10)
    quote2 = Quote.objects.create(text="Quote 2", source=source, likes=5)
    quote3 = Quote.objects.create(text="Quote 3", source=source, likes=15)

    url = reverse("quotes:top_quotes")
    response = client.get(url)

    assert response.status_code == 200
    assert "top_quotes" in response.context
    assert len(response.context["top_quotes"]) == 3

    top_quotes = response.context["top_quotes"]
    assert top_quotes[0].likes == 15
    assert top_quotes[1].likes == 10
    assert top_quotes[2].likes == 5
