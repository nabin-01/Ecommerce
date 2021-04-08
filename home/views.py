from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User


# the views are initialized in BaseView so, ItemDetailView and CategoryView inherits this initialization
# Create your views here.
class BaseView(View):
    # to inherit to other classes so it auto populates.
    views = dict()
    views['brand'] = Brand.objects.filter(status='active')
    views['count'] = []
    for i in views['brand']:
        count_brand = Item.objects.filter(brand=i.id).count()
        g = {'name': i.name, 'count': count_brand}
        views['count'].append(g)
    views['items'] = Item.objects.filter(status='active')
    views['item_count'] = Item.objects.count()
    views['count_cat'] = Category.objects.filter(status='active')
    views['cat_count'] = []
    for i in views['count_cat']:
        count_aria = Item.objects.filter(category=i.id).count()
        h = {'name': i.name, 'image': i.image, 'count': count_aria}
        views['cat_count'].append(h)
    # simply counts all item entries in Item model/database
    views['item_count'] = Item.objects.count()


class HomeView(BaseView):
    def get(self, request):
        self.views['categories'] = Category.objects.filter(status='active')
        self.views['sliders'] = Slider.objects.filter(status='active')
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

        # used slug id of item to get 1 single item
        self.views['item_detail'] = Item.objects.filter(slug=slug)

        # to display active user reviews
        self.views['reviews'] = Review.objects.filter(slug=slug, status='active')

        # to count user_reviews
        # self.views['reviews'] = Item.objects.filter(slug=slug, status='active')
        # self.views['rev_count'] = []
        # for i in self.views['reviews']:
        #     count_rev = Review.objects.filter(item_id=i.id).count()
        #     j = {'count': count_rev}
        #     self.views['rev_count'].append(j)
        # self.views['rating'] = Review.objects.filter(slug_reviewed_item=id)
        # slug_reviewed_id = Review.objects.filter(status='active').get(slug=slug).slug_reviewed_item_id
        # self.views['reviews'] = Item.objects.filter(id=slug_reviewed_id).get(slug=slug)

        # if len(str(Review.get(username=username))) < 3 or len(str(Review.get())) < 5 or len(msg) < 5:
        #     messages.error(request, 'Please re-submit the message!')
        # else:
        #     messages.success(request, '✔️Your message is successfully submitted!')

        # # to count total of each Brand items
        # # used status 'active' of item to get all active items of Brand model
        # self.views['brand'] = Brand.objects.filter(status='active')
        # # initialize list to pass as a value of 'count' key in dict views = {}
        # self.views['count'] = []
        # # loops through each brand
        # for i in self.views['brand']:
        #     # brand field of Item model searches for all same brand items,
        #     # by using Brand model primary key i.e. 'i.id' and counts all
        #     count_aria = Item.objects.filter(brand=i.id).count()
        #     # make a dict for storing necessary values
        #     d = {'name': i.name, 'count': count_aria}
        #     # appends dict 'd' to self.views['count'] list and makes values of 'count' keys
        #     self.views['count'].append(d)

        # # gets all items of status 'active'
        # self.views['items'] = Item.objects.filter(status='active')

        # # counts total of each Category items,
        # # By passing primary id of Category model to Item model which is same field.
        # # i.e. category field = category_id = id of Category Model
        # self.views['count_cat'] = Category.objects.filter(status='active')
        # self.views['cat_count'] = []
        # for i in self.views['count_cat']:
        #     count_aria = Item.objects.filter(category=i.id).count()
        #     e = {'name': i.name, 'image': i.image, 'cat_count': count_aria}
        #     self.views['cat_count'].append(e)

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
        if len(name) < 3 or len(sub) < 5 or len(msg) < 5:
            messages.error(request, 'Please re-submit the message!')
        else:
            data.save()
            messages.success(request, '✔️Your message is successfully submitted!')
        # views = dict()
        # views['message'] = 'The form is successfully submitted!'
        return render(request, 'contact.html')
    return render(request, 'contact.html')


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']
        fname = request.POST['fname']
        lname = request.POST['lname']

        if password == cpassword:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'This username is already taken!')
                return redirect('home:account')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'This email is already taken!')
                return redirect('home:account')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                    first_name=fname,
                    last_name=lname
                )
                user.save()
                messages.success(request, '✔️You are registered!')
                return redirect('/accounts/login')
        else:
            messages.error(request, 'These passwords do not match!')
            return redirect('home:account')
    return render(request, 'signup.html')


def review_item(request):
    if request.method == 'POST':
        rating = request.POST['rating']
        review = request.POST['review']
        username = request.user.username
        email = request.user.email
        slug = request.POST['slug']

        user_review = Review.objects.create(
            rating=rating,
            username=username,
            review=review,
            email=email,
            slug=slug
        )
        if rating < 1 or len(review) < 5:
            messages.error(request, 'Please re-submit the review!')
            return redirect('home:products')
        else:
            user_review.save()
            # to auto add a field while 'POST' from user, and it does not have to back-ended
            # instance = user_review.save(commit=False)
            # instance.author = instance.user # instance.user gets current user username
            # instance.save()
            messages.success(request, '✔️Your review is successfully submitted!')

            return redirect(f'/products/{slug}')
