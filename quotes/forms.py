from django import forms
from .models import Quote, Source


class QuoteForm(forms.ModelForm):
    """
    Форма для добавления цитаты, с выбором источника и валидацией
    (наличие в базе и ограничение в 3 цитаты из одного источника)
    """
    new_source = forms.CharField(
        max_length=100,
        required=False,
        label='Или введите название нового источника'
    )

    class Meta:
        model = Quote
        fields = ['text', 'source', 'weight']
        labels = {
            'text': 'Текст цитаты',
            'source': 'Выберите источник',
            'weight': 'Вес цитаты'
        }

        help_texts = {
            'weight': 'Чем выше вес, тем чаще цитата будет показываться на главной',
        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        source = cleaned_data.get('source')
        new_source_name = cleaned_data.get('new_source')

        if Quote.objects.filter(text=text).exists():
            raise forms.ValidationError("Такая цитата уже существует в базе!")

        final_source = source
        if new_source_name:
            final_source, created = Source.objects.get_or_create(name=new_source_name)

        if final_source and Quote.objects.filter(source=final_source).count() >= 3:
            raise forms.ValidationError(f"У источника '{final_source.name}' уже есть 3 цитаты. Лимит исчерпан.")

        cleaned_data['source'] = final_source
        return cleaned_data