from django.shortcuts import render, redirect
from .forms import QuoteForm
from .models import Quote

def random_quote_view(request):
    """
    Представление для вывода цитаты на основе менеджера модели Quote
    """
    selected_quote = Quote.objects.random()
    if selected_quote is None:
        return render(request, 'quotes/index.html', {
            'quote': None,
            'error': "В базе пока нет ни одной цитаты. Добавьте первую!"
        })

    selected_quote = Quote.objects.random()
    selected_quote.view_count += 1
    selected_quote.save()
    return render(request, 'quotes/index.html', {'quote': selected_quote})


def add_quote_view(request):
    """
    Представление для добавления цитаты из формы
    """
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('random_quote')
    else:
        form = QuoteForm()

    return render(request, 'quotes/add_quote.html', {'form': form})