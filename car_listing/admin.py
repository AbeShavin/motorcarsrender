from django.contrib import admin
from .models import CarMake, CarModel, Car


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

class CarMakeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

class CarModelAdmin(admin.ModelAdmin):
    list_display = ('name', 'make')
    list_filter = ('make',)
    search_fields = ('name', 'make__name')

class CarAdmin(admin.ModelAdmin):
    list_display = ('make', 'model', 'year', 'price')
    list_filter = ('make', 'model', 'year')
    search_fields = ('make__name', 'model__name', 'year', 'price')

admin.site.register(CarMake, CarMakeAdmin)
admin.site.register(CarModel, CarModelAdmin)
