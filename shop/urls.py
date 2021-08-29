from django.urls import path

from . import views

app_name = 'shop'
urlpatterns = [
    path('' , views.product_list_view , name='shop-home') ,
    path('<int:pk>/' , views.product_detail , name='product-detail') ,
    path('slider/' , views.slider_view , name='slider-example') ,
]
