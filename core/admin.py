from django.contrib import admin
from . import models


@admin.register(models.Images)
class ImagesAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.BillingAddress)
class BillingAddressAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Payment)
class PaymentAdmin(admin.ModelAdmin):
    pass


# @admin.register(models.PaymentInHome)
# class PaymentInHomeAdmin(admin.ModelAdmin):
#     pass


@admin.register(models.Information)
class InformationAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Video)
class VideoAdmin(admin.ModelAdmin):
    pass


@admin.register(models.News)
class NewsAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Contact)
class ContactAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    pass


class ImagesInline(admin.TabularInline):
    model = models.Images
    extra = 1


class InformationInline(admin.TabularInline):
    model = models.Information
    extra = 1


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImagesInline, InformationInline]
