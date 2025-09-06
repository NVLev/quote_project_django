from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        labels = {
            "username": "Имя пользователя",
            "email": "Email адрес",
        }
        help_texts = {
            "username": "Обязательное поле. Не более 150 символов. Только буквы, цифры и @/./+/-/_",
        }

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Пользователь с таким email уже существует.")
        return email
