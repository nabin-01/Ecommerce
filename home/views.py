from django.shortcuts import render
from django.views.generic.base import View
from .models import *


# Create your views here.
class BaseView(View):
    views = {}


class HomeView(BaseView):
    def get(self, request):
        self.views['categories'] = Category.objects.filter(status='active')
        self.views['sliders'] = Slider.objects.filter(status='active')
        self.views['brands'] = Brand.objects.filter(status='active')
        self.views['ads'] = Ad.objects.all()
        self.views['hots'] = Item.objects.filter(label='hot_product')
        self.views['news'] = Item.objects.filter(label='new')
        self.views['sales'] = Item.objects.filter(label='sale')
        self.views['defaults'] = Item.objects.filter(label='')
        return render(request, 'index.html', self.views)


class ListView(BaseView):
    def get(self, request):
        return render(request, 'product-list.html', self.views)


class ItemDetailView(BaseView):
    # dynamic ids are used for making dynamic - slug is used here
    def get(self, request, slug):
        self.views['item_detail'] = Item.objects.filter(slug=slug)
        self.views['brand'] = Brand.objects.filter(status='active')
        self.views['count'] = []
        for i in self.views['brand']:
            count_aria = Item.objects.filter(brand=i.id).count()
            d = {'name': i.name, 'count': count_aria}
            self.views['count'].append(d)

        self.views['count_cat'] = Category.objects.filter(status='active')
        self.views['cat_count'] = []
        for i in self.views['count_cat']:
            count_aria = Item.objects.filter(category=i.id).count()
            e = {'name': i.name, 'image': i.image, 'cat_count': count_aria}
            self.views['cat_count'].append(e)
        cat = Item.objects.get(slug=slug).category_id
        self.views['catitems'] = Item.objects.filter(category=cat)
        return render(request, 'product-detail.html', self.views)

