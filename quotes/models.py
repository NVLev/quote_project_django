from django.db import models
from itertools import count
from tkinter.constants import CASCADE

from django import forms
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.translation import ngettext

class Source(models.Model):
    """
    Модель Source представляет источник цитат
    """

    class Meta:
        ordering = ["-name"]
        verbose_name = _("Source")
        verbose_name_plural = _("Source")

    name = models.CharField(
        max_length=100,
        verbose_name=_("Name"),
        help_text=_("Enter source name"),
        db_index=True,
    )

    def __str__(self):
        return self.name

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
    def __str__(self):
        return self.text
