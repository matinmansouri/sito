from django.conf import settings
from django.db import models
from django.urls import reverse

CATEGORY_CHOICES = (
    ('M', 'مس'),
    ('B', 'برنج'),
    ('N', 'نقره'),
    ('A', 'ابزار'),
)


class Information(models.Model):
    title = models.CharField(max_length=255)
    body = models.CharField(max_length=255)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Images(models.Model):
    img = models.ImageField(upload_to='product/')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=2)
    price = models.IntegerField()
    discount_price = models.IntegerField(blank=True, null=True)
    description = models.TextField()
    keywordsGoogle = models.TextField(blank=True, null=True)
    keywordsSite = models.TextField(blank=True, null=True)
    singleImage = models.ImageField(upload_to='product/')
    Llikes = models.IntegerField(default=1)
    related = models.IntegerField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    # ShareOn
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("core:product", kwargs={'slug': self.slug})

    def get_add_to_cart_url(self):
        return reverse("core:add-to-cart", kwargs={'slug': self.slug})

    def get_remove_from_cart_url(self):
        return reverse("core:remove-from-cart", kwargs={'slug': self.slug})


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    oredered = models.BooleanField(default=False)
    item = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return self.item.title

    def get_total_item_price(self):
        return self.item.price

    def get_total_item_discount_price(self):
        return self.item.discount_price

    def get_amount_saved(self):
        if (self.item.discount_price):
            return self.get_total_item_price() - self.get_total_item_discount_price()
        else:
            return 0

    def get_final_price(self):
        if (self.item.discount_price):
            return self.get_total_item_discount_price()
        else:
            return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    oredered_date = models.DateTimeField()
    oredered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def get_total_amount_saved(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_amount_saved()
        return total

    def get_total(self):
        if (self.items.all().count() > 0):
            total = 0
            for order_item in self.items.all():
                total += order_item.get_final_price()
            if total < 300000:
                total += 9000
            return total
        else:
            return 0

    def get_orginalPrice(self):
        total = 0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        return total

    def get_total_in_rial(self):
        if (self.get_total() > 0):
            total = self.get_total()
            totalrial = str(total) + '0'
            return totalrial
        else:
            return 0


class BillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100, blank=True, null=True)
    zip = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=255, default='0')

    def __str__(self):
        return self.user.username


class Comment(models.Model):
    product = models.ForeignKey(Product, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return 'کامت از {} برای {}'.format(self.product, self.name)


class News(models.Model):
    emails = models.EmailField()

    def __str__(self):
        return self.emails


class Video(models.Model):
    url = models.TextField()
    created = models.DateTimeField(auto_now_add=True)


class Blog(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='Blog/')
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    day = models.CharField(max_length=255)
    month = models.CharField(max_length=255)
    year = models.CharField(max_length=255)
    user_FullName = models.CharField(max_length=255)
    related = models.IntegerField(blank=True, null=True)

    def get_absolute_url(self):
        return reverse("core:BlogDetail", kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=255)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
