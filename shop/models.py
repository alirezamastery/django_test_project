from django.db import models
import datetime
from django.utils import timezone
from django.conf import settings
from django.urls import reverse_lazy
from PIL import Image

# User = get_user_model()  <--for getting User in other places use this

# inside models.py import User like this:
User = settings.AUTH_USER_MODEL


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=20 , decimal_places=2 , default=0)
    image = models.ImageField(default='default.jpg' , upload_to='product_pics')
    description = models.TextField(default='')
    pub_date = models.DateTimeField(default=timezone.now)
    inventory = models.IntegerField(default=0)
    featured = models.BooleanField(default=False)
    is_digital = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    # you can implement any logic you want just like a normal python class
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    # in python methods are objects and can have their own attributes
    # and Django actually has usages for these attributes
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'

    # to be used in templates instead of hard coding the url
    def get_absolute_url(self):
        return reverse_lazy('shop:product-detail' , kwargs={'pk': self.pk})

    # change the picture size when saving an object of the model
    def save(self , **kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300 , 300)
            img.thumbnail(output_size)
            img.save(self.image.path)

    def get_rating(self):
        rating_qs = RatingModel.objects.all().filter(product=self)
        if len(rating_qs) == 0:
            return 0
        rating = 0
        for r in rating_qs:
            rating += r.rating
        return round(rating / len(rating_qs) , 1)

    def has_inventory(self):
        return self.inventory > 0  # True or False

    def remove_items_from_inventory(self , count=1 , save=True):
        current_inv = self.inventory
        current_inv -= count
        self.inventory = current_inv
        if save:
            self.save()
        return self.inventory


class RatingModel(models.Model):
    class rates(models.IntegerChoices):
        poor = 1
        Average = 2
        Good = 3
        Very_Good = 4
        Excellent = 5

    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name='product')
    product_user = models.ForeignKey(User , on_delete=models.CASCADE , related_name='product_user')
    rating = models.IntegerField(choices=rates.choices)

    def __str__(self):
        return f'Rating of {self.product.name} from {self.product_user.username} is {self.rating}'
