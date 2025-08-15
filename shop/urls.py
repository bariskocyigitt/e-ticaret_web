from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductListView.as_view(), name="products"),
    path("products/<slug:slug>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<slug:slug>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<slug:slug>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout_view, name="checkout"),
]
