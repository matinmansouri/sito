from django.urls import path
from . import views

app_name = 'core'
urlpatterns = [
    path('', views.index, name="index"),

    path('product/<slug>/', views.Product, name="product"),
    path('categories/<cat>/', views.Category, name="category"),
    path('like/<slug>/', views.Likes, name="Like"),
    path('news/', views.News, name="news"),
    path('tools/', views.Tools, name="Tools"),
    path('products/', views.ShopGrid, name="ShopGrid"),
    path('blog/', views.BlogList, name="BlogList"),
    path('blog/<slug>/', views.BlogDetail, name="BlogDetail"),
    path('contact-us/', views.Contact, name="Contact"),
    path('add-to-cart/<slug>', views.add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<slug>', views.remove_from_cart, name='remove-from-cart'),
    path('cart/', views.OrderSumaryView.as_view(), name='order-summary'),
    path('checkout/', views.CheckoutView.as_view(), name='checkout'),
    path('request/', views.send_request, name='request'),
    path('verify/', views.verify, name='verify'),
    path('ajax_calls/search/', views.autocompleteModel),
    path('search/', views.SearchResults, name="Search"),
    path('profile/', views.Profile, name='profile'),
]
