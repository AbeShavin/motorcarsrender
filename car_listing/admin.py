from django.contrib import admin
from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'price', 'zipcode')
    search_fields = ('make', 'model', 'year', 'price', 'zipcode')
    list_filter = ('make', 'model', 'year', 'price', 'zipcode')
    ordering = ('-created_at',)

    fieldsets = (
        (None, {
            'fields': ('owner', 'make', 'model', 'year', 'price', 'zipcode', 'latitude', 'longitude', 'description', 'image')
        }),
    )
