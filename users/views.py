from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm
from django.contrib.auth.forms import UserCreationForm
from quotes.models import Quote


def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('quotes:random_quote')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})


@login_required
def profile_view(request):
    return render(request, 'users/profile.html', {'user': request.user})


@login_required
def user_stats_view(request):
    user_quotes = Quote.objects.filter(author=request.user)
    total_quotes = user_quotes.count()
    total_likes = sum(quote.likes for quote in user_quotes)
    total_views = sum(quote.view_count for quote in user_quotes)

    return render(request, 'users/stats.html', {
        'user_quotes': user_quotes,
        'total_quotes': total_quotes,
        'total_likes': total_likes,
        'total_views': total_views,
    })
