import django_filters
from .models import Product
from django import forms


class ProductFilter(django_filters.FilterSet):
    choices = (
        ('-pub_date' , 'تاریخ جدید به قدیم') ,
        ('pub_date' , 'تاریخ قدیم به جدید') ,
        ('price' , 'قیمت کمترین به بیشترین') ,
        ('-price' , 'قیمت بیشترین به کمترین') ,
    )
    ordering_by = django_filters.ChoiceFilter(choices=choices ,
                                              label='مرتب سازی بر اساس' ,
                                              widget=forms.RadioSelect ,
                                              empty_label=None ,  # so "-------" won't show up as default
                                              method='filter_choices_order_by')

    class Meta:
        model = Product
        fields = {
            # 'ordering_by',
            'price': ['lte' , 'gte'] ,
        }

    @staticmethod
    def filter_choices_order_by(queryset , name , value):
        return queryset.order_by(value)

    @staticmethod
    def filter_price_range(queryset , name , value):
        print(name)
        print('*' * 200)
        return queryset.order_by(value)

