from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path , include

from django.views.generic import TemplateView

urlpatterns = [
    path('admin/' , admin.site.urls , name='admin-page') ,

    # users:    (be careful to not have conflicting urls in users and blog)
    path('' , include('users.urls')) ,
    # blog:
    path('' , include('blog.urls')) ,
    # polls:
    path('polls/' , include('polls.urls')) ,
    # shop:
    path('shop/' , include('shop.urls')) ,
    # orders:
    path('orders/' , include('orders.urls')) ,
    # tweet:
    # path('api/tweets/' , include('tweet.urls')) ,
    # react:
    # path('react/' , TemplateView.as_view(template_name='react_via_dj.html') , name='react-page') ,
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL , document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL , document_root=settings.STATIC_ROOT)
