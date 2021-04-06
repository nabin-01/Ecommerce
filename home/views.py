from django.shortcuts import render
from django.views.generic.base import View
from .models import *
from django.contrib import messages


# Create your views here.
class BaseView(View):
    # to inherit to other classes so it auto populates.
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


# class ListView(BaseView):
#     def get(self, request):
#         # render to pass dict in html
#         return render(request, 'category.html', self.views)


class ItemDetailView(BaseView):
    # dynamic ids are used for making dynamic - slug is used here
    def get(self, request, slug):
        # self.views['rating'] = Item.objects.filter(rating=rating)
        # used slug id of item to get 1 single item
        self.views['item_detail'] = Item.objects.filter(slug=slug)
        # to count total of each Brand items
        # used status 'active' of item to get all active items of Brand model
        self.views['brand'] = Brand.objects.filter(status='active')
        # initialize list to pass as a value of 'count' key in dict views = {}
        self.views['count'] = []
        # loops through each brand
        for i in self.views['brand']:
            # brand field of Item model searches for all same brand items,
            # by using Brand model primary key i.e. 'i.id' and counts all
            count_aria = Item.objects.filter(brand=i.id).count()
            # make a dict for storing necessary values
            d = {'name': i.name, 'count': count_aria}
            # appends dict 'd' to self.views['count'] list and makes values of 'count' keys
            self.views['count'].append(d)
        # gets all items of status 'active'
        self.views['items'] = Item.objects.filter(status='active')
        # simply counts all item entries in Item model/database
        self.views['item_count'] = Item.objects.count()
        # counts total of each Category items,
        # By passing primary id of Category model to Item model which is same field.
        # i.e. category field = category_id = id of Category Model
        self.views['count_cat'] = Category.objects.filter(status='active')
        self.views['cat_count'] = []
        for i in self.views['count_cat']:
            count_aria = Item.objects.filter(category=i.id).count()
            e = {'name': i.name, 'image': i.image, 'cat_count': count_aria}
            self.views['cat_count'].append(e)
        # used slug id to get exact item and its category_id
        # to get related same category products
        cat = Item.objects.get(slug=slug).category_id
        self.views['catitems'] = Item.objects.filter(category=cat)
        return render(request, 'product-detail.html', self.views)


class CategoryView(BaseView):
    def get(self, request, slug):
        # slug id used to get exact that category and .id gets its category id
        cat_id = Category.objects.get(slug=slug).id
        self.views['catdetail'] = Item.objects.filter(category=cat_id)
        return render(request, 'product-list.html', self.views)


class SearchView(BaseView):
    def get(self, request):
        # query = request.GET.get('search', None)
        if request.method == 'GET':
            query = request.GET['search']
            self.views['search_product'] = Item.objects.filter(title__icontains=query)
            return render(request, 'search.html', self.views)
        return render(request, 'search.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        sub = request.POST['subject']
        msg = request.POST['message']

        data = Contact.objects.create(
            name=name,
            email=email,
            subject=sub,
            message=msg
        )
        # check entered user data is correct or not by python validators
        # saves form data to DB
        if len(name) < 3 or len(msg) < 4:
            data.save()
            messages.error(request, 'Please re-submit the form!')
        else:
            messages.success(request, 'The form is successfully submitted!')
        # views = dict()
        # views['message'] = 'The form is successfully submitted!'
        return render(request, 'contact.html')
    return render(request, 'contact.html')


