import random
from itertools import count
from tkinter.constants import CASCADE

from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.db.models.aggregates import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext


class Source(models.Model):
    """Модель представляет источник цитат"""

    SOURCE_TYPES = [
        ("movie", "Фильм"),
        ("book", "Книга"),
        ("play", "Спектакль"),
        ("other", "Другое"),
    ]

    name = models.CharField(max_length=100, db_index=True)
    type = models.CharField(max_length=20, choices=SOURCE_TYPES, default="other")

    class Meta:
        ordering = ["name"]
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    def __str__(self):
        return f"{self.name} ({self.get_type_display()})"


class QuoteManager(models.Manager):
    """Менеджер для модели Quotes
    настраивает вывод цитат в соответствии с весом"""

    def random(self):
        quotes = list(self.all())
        if not quotes:
            return None

        total_weight = sum(q.weight for q in quotes)
        if total_weight == 0:
            return random.choice(quotes)

        random_index = random.uniform(0, total_weight)
        current = 0

        for quote in quotes:
            current += quote.weight
            if current > random_index:
                return quote

        return random.choice(quotes)


class Quote(models.Model):
    """
    Модель Quote представляет цитаты
    """

    class Meta:
        verbose_name = _("Quote")
        verbose_name_plural = _("Quote")

    text = models.TextField(unique=True)
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    base_weight = models.PositiveIntegerField(default=5)
    view_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    author = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Автор"
    )

    objects = QuoteManager()

    @property
    def weight(self):
        """Динамический вес: номинальный + лайки - дизлайки"""
        return max(1, self.base_weight + self.likes - self.dislikes)

    def __str__(self):
        return self.text
