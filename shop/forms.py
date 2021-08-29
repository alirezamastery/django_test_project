from django import forms
from .models import RatingModel


class RatingModelForm(forms.ModelForm):
    class Meta:
        model = RatingModel
        fields = ['rating']


class ProductOrderingForm(forms.Form):
    choices = (
        ('-pub_date' , 'تاریخ جدید به قدیم') ,
        ('pub_date' , 'تاریخ قدیم به جدید') ,
        ('price' , 'قیمت کمترین به بیشترین') ,
        ('-price' , 'قیمت بیشترین به کمترین') ,
    )
    ordering = forms.ChoiceField(choices=choices , widget=forms.RadioSelect , required=False ,
                                 label='مرتب سازی بر اساس')

class ProductFilterForm(forms.Form):
    has_inventory = forms.BooleanField(required=False , label='فقط کالاهای موجود')

class FilterForm(forms.Form):
    price = forms.IntegerField(initial=0)
