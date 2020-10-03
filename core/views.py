from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic.base import View
from django.conf import settings
from django.core.paginator import Paginator
from django.core.exceptions import ObjectDoesNotExist
from zeep import Client
from core import models, forms

import json


def latestproducts():
    return models.Product.objects.all().order_by('-created')[:10]


def index(request):
    # Likes
    mostLike = models.Product.objects.all().order_by('-Llikes')[:10]
    # lastProduct
    lastestProductList = latestproducts()
    # Video
    Video = models.Video.objects.all().order_by('-created')[:1]
    # Blog
    lastBlogList = models.Blog.objects.all().order_by('-created')[:3]
    # Products
    getPro = models.Product.objects.all()
    m = []
    b = []
    n = []
    for product in getPro:
        if product.category == 'M':
            m.append(product)
        elif product.category == 'B':
            b.append(product)
        elif product.category == 'N':
            n.append(product)

    context = {
        'blog': lastBlogList,
        'mostLikeStart': mostLike[:5],
        'mostLikeEnd': mostLike[5:10],
        'lastest': lastestProductList,
        'lastestproductendstartlist': lastestProductList[:5],
        'lastestproductendendlist': lastestProductList[5:10],
        "m": m[:4],
        "b": b[:4],
        "n": n[:4],
        'url': Video
    }
    return render(request, 'core/index.html', context)


def Product(request, slug):
    product = get_object_or_404(models.Product, slug=slug)
    productsRel = models.Product.objects.filter(related=product.related)
    relatedProducts = productsRel.filter(~Q(id=product.id))
    images = models.Images.objects.filter(product=product)
    information = models.Information.objects.filter(product=product)
    comments = product.comments.filter(active=True)
    new_comment = False

    if request.method == 'POST' and 'CB' in request.POST:
        comment_form = forms.CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.product = product
            new_comment.save()
    else:
        comment_form = forms.CommentForm()

    context = {
        'comments': comments,
        'comments_form': comment_form,
        'new_comment': new_comment,
        'product': product,
        "related": relatedProducts[:4],
        'images': images,
        'Information': information,
    }
    return render(request, 'core/product.html', context)


def Category(request, cat):
    products = models.Product.objects.filter(category=cat)
    productsCounter = models.Product.objects.filter(category=cat).count()
    paginator = Paginator(products, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    category = ''
    if cat == 'M':
        category = 'مس'
    elif cat == 'B':
        category = 'برنج'
    elif cat == 'N':
        category = 'نقره'
    else:
        return redirect('core:index')

    context = {
        'count': productsCounter,
        'cat': category,
        'page_obj': page_obj,
        "page_range": paginator.page_range,
    }
    return render(request, 'core/list.html', context)


def Likes(request, slug):
    n = get_object_or_404(models.Product, slug=slug)
    n.Llikes = n.Llikes + 1
    n.save()
    return redirect('core:product', n.slug)


def News(request):
    query = request.GET.get('q')
    n = models.News(emails=query)
    n.save()
    return redirect("/")


def Tools(request):
    products = models.Product.objects.filter(category='A')
    productsCounter = models.Product.objects.filter(category='A').count()
    paginator = Paginator(products, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'count': productsCounter,
        "cat": "ابزار ها",
        "pageConditionTools": True,
        'page_obj': page_obj,
        "page_range": paginator.page_range,
    }
    return render(request, 'core/list.html', context)


def ShopGrid(request):
    products = models.Product.objects.filter(~Q(category='A'))
    productsCounter = models.Product.objects.filter(~Q(category='A')).count()
    paginator = Paginator(products, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'count': productsCounter,
        "cat": "محصولات",
        "pageConditionShop": True,
        'page_obj': page_obj,
        "page_range": paginator.page_range,
    }
    return render(request, 'core/list.html', context)


def BlogList(request):
    lastBlogList = models.Blog.objects.all().order_by('-created')[:5]
    posts = models.Blog.objects.all()

    paginator = Paginator(posts, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'lastBlog': lastBlogList,
        "count": posts.count(),
        'page_obj': page_obj,
        "page_range": paginator.page_range,
    }

    return render(request, 'core/blogList.html', context)


def BlogDetail(request, slug):
    post = get_object_or_404(models.Blog, slug=slug)
    postRels = models.Blog.objects.filter(related=post.related)
    relatedProducts = postRels.filter(~Q(id=post.id))

    context = {
        'post': post,
        'relatedPost': relatedProducts[:3],
    }
    return render(request, 'core/blogDetails.html', context)


def Contact(request):
    # main
    if request.method == 'POST' and 'send' in request.POST:
        contact = forms.ContactForm(request.POST)
        if contact.is_valid():
            con = models.Contact(name=contact.cleaned_data['name'],
                                 email=contact.cleaned_data['email'],
                                 body=contact.cleaned_data['body'])
            con.save()
            messages.success(request, "فرم شما با موفقیت ارسال شد.")
            return redirect("/contact-us/")
    else:
        contact = forms.ContactForm()
    context = {
        'contact': contact,
    }
    return render(request, 'core/contact.html', context)


MERCHANT = settings.ZARINPAL_SECERT_KEY
client = Client('https://www.zarinpal.com/pg/services/WebGate/wsdl')
amount = 0  # Toman / Required
description = "ممنونم بابت خرید از فروشگاه سیتوپلاس"  # Required
email = 'info@sitoplusgallery'  # Optional
mobile = '09123456789'  # Optional
CallbackURL = 'http://127.0.0.1:8000/verify/'  # Important: need to edit for realy server.


def SetAmount(amountval):
    amount = amountval
    return amount


def send_request(request):
    order = models.Order.objects.get(user=request.user, oredered=False)
    amount = SetAmount(int(order.get_total()))
    result = client.service.PaymentRequest(MERCHANT, amount, description, email, mobile, CallbackURL)
    if result.Status == 100:
        return redirect('https://www.zarinpal.com/pg/StartPay/' + str(result.Authority))
    else:
        return HttpResponse('Error code: ' + str(result.Status) + '\n خطایی رخ داده است ')


def verify(request):
    order = models.Order.objects.get(user=request.user, oredered=False)
    if request.GET.get('Status') == 'OK':
        result = client.service.PaymentVerification(MERCHANT, request.GET['Authority'], amount)
        if result.Status == 100:
            # payment = Payment()
            # payment.stripe_charge_id = str(result.RefID)
            # payment.user = request.user
            # payment.amount = amount
            # payment.save()
            # order.oredered = True
            # order.payment = payment
            # order.save()
            return HttpResponse('Transaction success.\nRefID: ' +
                                str(result.RefID) +
                                '\n عملیات انجام شد و به زودی محصول شما برای شما فرستاده میشود')
        elif result.Status == 101:
            return HttpResponse('Transaction submitted : ' + str(result.Status) + '\n معامله ارسال شد')
        else:
            return HttpResponse('Transaction failed.\nStatus: ' + str(result.Status) + '\n خطایی رخ داده است')
    else:
        payment = models.Payment()
        payment.stripe_charge_id = 'asdasd6623'
        payment.user = request.user
        payment.amount = amount
        payment.save()
        order.oredered = True
        order.payment = payment
        order.save()
        return HttpResponse('معاملات توسط کاربر انجام نشد یا لغو شد')


class OrderSumaryView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            order = models.Order.objects.get(user=self.request.user, oredered=False)
            context = {
                'object': order
            }
            return render(self.request, 'core/cart.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "شما سفارش فعال ندارید.")
            return redirect("/")


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(models.Product, slug=slug)
    order_item, created = models.OrderItem.objects.get_or_create(item=item,
                                                                 user=request.user,
                                                                 oredered=False)
    order_qs = models.Order.objects.filter(user=request.user, oredered=False)
    if (order_qs.exists()):
        order = order_qs[0]
        if (order.items.filter(item__slug=item.slug).exists()):
            messages.info(request, "This item quantity was updated.")
        else:
            messages.info(request, "این محصول به سبد خرید شما اضافه شد.")
            order.items.add(order_item)
    else:
        order_date = timezone.now()
        order = models.Order.objects.create(user=request.user, oredered_date=order_date)
        order.items.add(order_item)
        messages.info(request, "این محصول به سبد خرید شما اضافه شد.")
    return redirect("core:order-summary")


@login_required
def remove_from_cart(request, slug):
    item = get_object_or_404(models.Product, slug=slug)
    order_qs = models.Order.objects.filter(user=request.user, oredered=False)
    if (order_qs.exists()):
        order = order_qs[0]
        if (order.items.filter(item__slug=item.slug).exists()):
            order_item = models.OrderItem.objects.filter(item=item, user=request.user, oredered=False)[0]
            order.items.remove(order_item)
            messages.info(request, "این محصول از سبد خرید شما حذف شد.")
            return redirect("core:order-summary")
        else:
            messages.info(request, "این محصول در سبد خرید شما وجود ندارد.")
            return redirect("core:order-summary")
    else:
        messages.info(request, "شما سفارش فعال ندارید.")
        return redirect("core:order-summary")


class CheckoutView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = forms.CheckoutForm()
        try:
            order = models.Order.objects.get(user=self.request.user, oredered=False)
            context = {
                'object': order,
                'form': form
            }
            return render(self.request, 'core/checkout.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "شما سفارش فعال ندارید.")
            return redirect("/")

    def post(self, *args, **kwargs):
        form = forms.CheckoutForm(self.request.POST or None)
        try:
            order = models.Order.objects.get(user=self.request.user, oredered=False)
            if (form.is_valid()):
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                zip = form.cleaned_data.get('zip')
                firstname = form.cleaned_data.get('firstname')
                lastname = form.cleaned_data.get('lastname')
                PhoneNuber = form.cleaned_data.get('phonenumber')
                billing_address = models.BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment_address=apartment_address,
                    zip=zip,
                    firstname=firstname,
                    lastname=lastname,
                    phone_number=PhoneNuber,
                )
                billing_address.save()
                order.billing_address = billing_address
                order.save()
                return redirect('core:request')
            else:
                messages.warning(self.request, "پرداخت ناموفق.")
                return redirect("core:checkout")
        except ObjectDoesNotExist:
            messages.warning(self.request, "شما سفارش فعال ندارید.")
            return redirect("core:order-summary")


@login_required
def Profile(request):
    if request.user.is_superuser:
        orders = models.Order.objects.all().filter(oredered=True)
        for order in orders:
            print(order.billing_address.firstname)
        context = {
            'orders': orders,
        }
        return render(request, 'core/usermanaging.html', context)
    else:
        order = models.Order.objects.all().filter(user=request.user, oredered=True)

        context = {
            'orders': order,
        }
        return render(request, 'core/Profile.html', context)


def autocompleteModel(request):
    if request.is_ajax():
        q = request.GET.get('term', '').capitalize()
        search_qs = models.Product.objects.filter(
            Q(title__icontains=q) | Q(keywordsSite__icontains=q)
        )
        results = []
        for r in search_qs:
            results.append(r.title)
        data = json.dumps(results)
        print(data)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def SearchResults(request):
    try:
        query = request.GET.get('txtSearch')
        object_list = models.Product.objects.filter(
            Q(title__icontains=query) | Q(keywordsSite__icontains=query)
        )
        context = {
            "page_obj": object_list,
            "count": object_list.count(),
            "cat": query,
            "search": True
        }
        return render(request, "core/list.html", context)
    except ValueError:
        raise Http404("Not Found")
