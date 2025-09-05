from django.contrib import admin
from .models import Source, Quote


admin.site.register(Source)



@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ('text', 'source', 'base_weight', 'view_count', 'likes', 'dislikes')

    search_fields = ('text',)

    list_filter = ('source', 'base_weight')

    fieldsets = (
        (None, {
            'fields': ('text', 'source')
        }),
        ('Статистика и вес', {
            'fields': ('base_weight', 'view_count', 'likes', 'dislikes'),
            'classes': ('collapse',)
        }),
    )
