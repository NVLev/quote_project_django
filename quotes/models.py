from django.db import models
from itertools import count
from tkinter.constants import CASCADE
import random
from django import forms
from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

class Source(models.Model):
    """
    Модель Source представляет источник цитат
    """

    class Meta:
        ordering = ["name"]
        verbose_name = _("Source")
        verbose_name_plural = _("Sources")

    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Enter source name"),
        db_index=True,
    )

    def __str__(self):
        return self.name

class QuoteManager(models.Manager):
    """Менеджер для модели Quotes
        настраивает вывод цитат в соответствии с весом"""
    def random(self):
        total_weight = self.aggregate(total=Sum('weight'))['total']
        if total_weight is None or total_weight == 0:
            return random.choice(self.all()) if self.exists() else None

        random_index = random.uniform(0, total_weight)
        current = 0

        for quote in self.all():
            current += quote.weight
            if current > random_index:
                return quote

        return random.choice(self.all())

class Quote(models.Model):
    """
    Модель Quote представляет цитаты
    """
    class Meta:
        verbose_name = _("Quote")
        verbose_name_plural = _("Quote")

    text = models.TextField(unique=True)
    source = models.ForeignKey(
        Source,
        on_delete=models.CASCADE,
    )
    weight = models.PositiveIntegerField(default=1)
    view_count = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    objects = QuoteManager()
    def __str__(self):
        return self.text
