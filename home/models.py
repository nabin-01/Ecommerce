from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
# first_one -> stored in db, second_one -> what users see in html
# python_tuples
STATUS = (('active', 'active'), ('passive', 'passive'))
LABEL = (('new', 'new'), ('hot_product', 'hot_product'), ('sale', 'sale'), ('default', 'default'))


# reverse for passing kwargs(dict) in url
# slug = category certain id/ URL tags
# Category is subclass of models.model class
class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    slug = models.CharField(max_length=100, unique=True)
    status = models.CharField(choices=STATUS, max_length=200)
    # __str__ to return/give string as 'name' field when creating any model/object in the admin panel

    def __str__(self):
        return self.name

    # reverse helps to pass kwargs dict to specific url
    def get_cat_url(self):
        return reverse('home:category', kwargs={'slug': self.slug})


class Slider(models.Model):
    name = models.CharField(max_length=300)
    image = models.ImageField(upload_to='media/')
    description = models.TextField(blank=True)
    status = models.CharField(choices=STATUS, max_length=200)

    def __str__(self):
        return self.name


class Ad(models.Model):
    name = models.CharField(max_length=200)
    rank = models.IntegerField()
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='media/')
    status = models.CharField(choices=STATUS, max_length=200)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='media/')
    status = models.CharField(choices=STATUS, max_length=200)

    def __str__(self):
        return self.name


class Item(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    discounted_price = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(default=0, null=True, blank=True)
    label = models.CharField(choices=LABEL, max_length=200)
    image = models.ImageField(upload_to='media/')
    status = models.CharField(choices=STATUS, max_length=200)
    slug = models.CharField(max_length=100, unique=True)
    # when Category is deleted, Item/s also gets deleted
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    description = models.TextField(blank=True)
    specification = models.TextField(blank=True)

    def __str__(self):
        return self.title

    # reverse helps to pass kwargs dict to specific url
    def get_item_url(self):
        return reverse('home:products', kwargs={'slug': self.slug})


class Contact(models.Model):
    name = models.CharField(max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    subject = models.TextField(blank=True)
    message = models.TextField()

    def __str__(self):
        return self.name


class Review(models.Model):
    username = models.CharField(max_length=100, blank=True)
    email = models.EmailField(max_length=200, blank=True)
    review = models.TextField()
    rating = models.IntegerField(default=1)
    date_posted = models.DateTimeField(default=timezone.now)
    status = models.CharField(default='active', choices=STATUS, max_length=200)
    slug = models.CharField(max_length=200)
    item_review = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.username
