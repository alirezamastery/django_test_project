from django.shortcuts import render , redirect , get_object_or_404
from django.urls import reverse
from django.http import HttpResponse , HttpResponseRedirect
from django.contrib import messages
from django.views import generic
from .models import Product , RatingModel
from .forms import RatingModelForm , ProductOrderingForm , FilterForm , ProductFilterForm
from django.core.paginator import Paginator
from django.utils import timezone
from .filters import ProductFilter
from django_filters.views import FilterView
from django.http import QueryDict


# TODO can I use CBV with the features I want?
class ProductListView(generic.ListView):
    model = Product
    template_name = 'shop/home.html'
    context_object_name = 'products'
    ordering = ['-price']
    paginate_by = 6
    form_class = ProductOrderingForm

    def get(self , request , *args , **kwargs):
        product_list = Product.objects.order_by('-pub_date')
        ordering_form = self.form_class()

        paginator = Paginator(product_list , 12)  # Show 12 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'page_obj':      page_obj ,
            'ordering_form': ordering_form ,
            'products':      product_list ,
            'is_paginated':  True
        }
        return render(request , self.template_name , context)

    def post(self , request , *args , **kwargs):
        ordering_form = self.form_class(request.POST)
        if ordering_form.is_valid():
            # <process form cleaned data>
            ordering_choice = ordering_form.cleaned_data.get('ordering')
            product_list = Product.objects.order_by(f'{ordering_choice}')
            # return HttpResponseRedirect(request.path_info)
        context = {
            'ordering_form': ordering_form ,
            'products':      product_list ,
        }

        return render(request , self.template_name , context)

    def get_context_data(self , **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Shop'
        return context

    def get_queryset(self , *args , **kwargs):
        return Product.objects.order_by('-pub_date')


# TODO can I use request.session for ordering of this page?
# TODO pagination does not work (one problem is object filtering interferes with pagination: read saved articles)
def product_list_view(request):
    product_list = Product.objects.all()

    request_for_form = QueryDict(mutable=True)
    if 'ordering' in request.GET:
        request_for_form['ordering'] = request.GET['ordering']
    order_by_form = ProductOrderingForm(request_for_form or None)

    if order_by_form.is_valid():
        ordering_choice = order_by_form.cleaned_data.get('ordering')
        product_list = Product.objects.order_by(ordering_choice)

    paginate_by = 9
    paginated_filtered_products = Paginator(product_list , paginate_by)
    page_number = request.GET.get('page')
    product_page_obj = paginated_filtered_products.get_page(page_number)

    is_paginated = False
    if len(product_list) > paginate_by:
        is_paginated = True

    context = {
        'order_by_form':    order_by_form ,
        'product_page_obj': product_page_obj ,
        'is_paginated':     is_paginated
    }
    return render(request , 'shop/home.html' , context)


# TODO add price range slider
def show_products(request):
    context = dict()
    filtered_products = ProductFilter(request.GET , queryset=Product.objects.all())
    context['filtered_products'] = filtered_products

    paginated_filtered_products = Paginator(filtered_products.qs , 6)
    page_number = request.GET.get('page')
    product_page_obj = paginated_filtered_products.get_page(page_number)
    context['product_page_obj'] = product_page_obj

    return render(request , 'shop/product_all.html' , context)


def product_detail(request , pk):
    product_obj = get_object_or_404(Product , pk=pk)
    try:
        rate_obj = RatingModel.objects.get(product=product_obj , product_user=request.user)
    except:
        rate_obj = None
    # rating of product:
    rate_form = RatingModelForm(request.POST or None , instance=rate_obj)
    if rate_form.is_valid():
        user = request.user
        choice = rate_form.cleaned_data.get('rating')
        update_values = {'rating': choice}
        rate_obj , created = RatingModel.objects.update_or_create(product=product_obj ,
                                                                  product_user=user ,
                                                                  defaults=update_values)
        print(f'created new rating: {created}')
        messages.success(request , f'Your choice has been saved: {choice}')
        return HttpResponseRedirect(request.path_info)
    else:
        rate_form = RatingModelForm(instance=rate_obj)

    context = {
        'object':    product_obj ,
        'rate_form': rate_form ,
    }
    return render(request , 'shop/product_detail.html' , context)


def slider_view(request):
    return render(request , 'shop/slider.html')
