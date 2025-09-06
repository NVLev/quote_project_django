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
        label="Новый источник (название)"
    )
    new_source_type = forms.ChoiceField(
        choices=Source.SOURCE_TYPES,
        required=False,
        label="Тип источника"
    )

    class Meta:
        model = Quote
        fields = ['text', 'source', 'base_weight']
        labels = {
            'text': 'Текст цитаты',
            'source': 'Выберите источник',
            'base_weight': 'Вес цитаты'
        }

        help_texts = {
            "base_weight": "Начальный вес цитаты = 5. "
                           "Дальше вес изменяется автоматически: "
                           "лайк увеличивает, дизлайк уменьшает.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["base_weight"].disabled = True
        self.fields["base_weight"].initial = 5
        self.fields['source'].required = False
        self.fields['source'].empty_label = "--- Выберите источник ---"

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        source = cleaned_data.get("source")
        new_source_name = cleaned_data.get("new_source")
        new_source_type = cleaned_data.get("new_source_type")

        if Quote.objects.filter(text=text).exists():
            raise forms.ValidationError("Такая цитата уже существует в базе!")

        if not source and not new_source_name:
            raise forms.ValidationError(
                "Нужно либо выбрать существующий источник, либо ввести новый!"
            )
        if source and new_source_name:
            raise forms.ValidationError(
                "Нельзя одновременно выбрать источник и ввести новый!"
            )

        final_source = None

        if source:
            final_source = source

        elif new_source_name:
            source_type = new_source_type or "other"
            final_source, created = Source.objects.get_or_create(
                name=new_source_name.strip(),
                defaults={"type": source_type}
            )
        if final_source is None:
            raise forms.ValidationError("Произошла ошибка при определении источника. Попробуйте еще раз.")

        if Quote.objects.filter(source=final_source).count() >= 3:
            raise forms.ValidationError(f"У источника '{final_source.name}' уже есть 3 цитаты. Лимит исчерпан.")

        cleaned_data["source"] = final_source
        return cleaned_data

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user and user.is_authenticated:
            instance.author = user
        if commit:
            instance.save()
        return instance