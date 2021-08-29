from django.contrib import admin
from .models import Product , RatingModel


class ProductAdmin(admin.ModelAdmin):
    # fieldsets = [
    #     ('Price' , {'fields': ['price']})
    # ]
    list_display = ('name' , 'price' , 'pub_date')
    list_filter = ['name' , 'price' , 'pub_date']
    search_fields = ['name']


admin.site.register(Product , ProductAdmin)
admin.site.register(RatingModel)
