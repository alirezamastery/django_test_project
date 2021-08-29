from django.test import TestCase
from django.urls import reverse

from django.contrib.auth import get_user_model
from .models import Product , RatingModel

User = get_user_model()


class RatingModelTests(TestCase):

    def setUp(self):
        user_a = User.objects.create(username='alireza2' , email='ff@tt.com')
        user_a.is_staff = True
        user_a.is_superuser = True
        user_a.set_password('123456')
        user_a.save()

    def test_user_exists(self):
        user_count = User.objects.all().count()
        print(user_count)
        self.assertEqual(user_count , 1)

    def test_product_detail(self):
        product = Product.objects.create(name='y' , price='100' , description='')
        url = reverse('shop:product-detail' , args=(product.id ,))
        response = self.client.get(url)
        self.assertContains(response , product.price)
