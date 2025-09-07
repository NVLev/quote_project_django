import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from users.decorators import vote_login_required

from .forms import QuoteForm
from .models import Quote

logger = logging.getLogger(__name__)


def random_quote_view(request):
    """
    Представление для вывода цитаты на основе менеджера модели Quote
    """
    selected_quote = Quote.objects.random()
    if selected_quote is None:
        return render(
            request,
            "quotes/index.html",
            {"quote": None, "error": "В базе пока нет ни одной цитаты. Добавьте первую!"},
        )

    selected_quote = Quote.objects.random()
    selected_quote.view_count += 1
    selected_quote.save()
    return render(request, "quotes/index.html", {"quote": selected_quote})


def add_quote_view(request):
    """
    Представление для добавления цитаты из формы
    """
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save(user=request.user)
            return redirect("quotes:random_quote")
    else:
        form = QuoteForm()

    return render(request, "quotes/add_quote.html", {"form": form})


@vote_login_required
def like_quote_view(request, quote_id):
    """
    Представление для лайков.
    Увеличивает счетчик лайков цитаты.
    """
    quote = get_object_or_404(Quote, id=quote_id)
    session_key = f"voted_quote_{quote_id}"
    if not request.session.get(session_key):
        quote.likes += 1
        quote.save()
        request.session[session_key] = True
        messages.success(request, "Ваш голос учтен!")
        logger.info("Лайк успешно добавлен")
    else:
        messages.success(request, "Вы уже голосовали за эту цитату!")
        logger.info("Лайк уже добавлялся в этой сессии")
    return redirect("quotes:random_quote")


@vote_login_required
def dislike_quote_view(request, quote_id):
    """
    Представление для дизлайков.
    Увеличивает счетчик дизлайков цитаты.
    """
    quote = get_object_or_404(Quote, id=quote_id)
    session_key = f"voted_quote_{quote_id}"
    if not request.session.get(session_key):
        quote.dislikes += 1
        quote.save()
        request.session[session_key] = True
        messages.success(request, "Ваш голос учтен!")
        logger.info("Дизлайк успешно добавлен")
    else:
        messages.success(request, "Вы уже голосовали за эту цитату!")
        logger.info("Дизлайк уже добавлялся в этой сессии")
    return redirect("quotes:random_quote")


def top_quotes_view(request):
    """
    Представление для страницы самых "весомых" цитат
    """
    top_quotes = Quote.objects.all().order_by("-likes")[:10]

    return render(
        request,
        "quotes/top_quotes.html",
        {"top_quotes": top_quotes, "title": "Топ-10 цитат по лайкам"},
    )
