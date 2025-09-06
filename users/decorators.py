from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect


def vote_login_required(function=None):
    """
    Декоратор, который перенаправляет анонимных пользователей на страницу входа
    с сообщением о необходимости авторизации
    """

    def check_user_and_message(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "🔐 Чтобы голосовать, пожалуйста, войдите в систему")
            return redirect(f"{settings.LOGIN_URL}?next={request.path}")
        return function(request, *args, **kwargs)

    return check_user_and_message if function else check_user_and_message
