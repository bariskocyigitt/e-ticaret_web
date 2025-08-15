from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import DetailView, ListView

from .forms import AddToCartForm, CheckoutForm, SignUpForm
from .models import Order, OrderItem, Product

CART_KEY = "cart"


def _get_cart(request):
    return request.session.get(CART_KEY, {})


def _save_cart(request, cart):
    request.session[CART_KEY] = cart
    request.session.modified = True


# ---------- SAYFALAR ----------

# İlk ekran: girişli değilse kayıt sayfasına yönlendir
def home(request):
    if not request.user.is_authenticated:
        return redirect("signup")
    products = Product.objects.filter(is_active=True).order_by("-created_at")[:6]
    return render(request, "home.html", {"products": products})


def about(request):
    return render(request, "about.html")


class ProductListView(ListView):
    model = Product
    template_name = "products_list.html"
    context_object_name = "products"


class ProductDetailView(DetailView):
    model = Product
    template_name = "product_detail.html"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["form"] = AddToCartForm()
        return ctx


# ---------- SEPET ----------

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    form = AddToCartForm(request.POST or None)
    if form.is_valid():
        qty = form.cleaned_data["quantity"]
        cart = _get_cart(request)
        cart[slug] = cart.get(slug, 0) + qty
        _save_cart(request, cart)
        messages.success(request, "Ürün sepete eklendi!")
    return redirect("product_detail", slug=slug)


def remove_from_cart(request, slug):
    cart = _get_cart(request)
    if slug in cart:
        cart.pop(slug)
        _save_cart(request, cart)
        messages.info(request, "Ürün sepetten çıkarıldı.")
    return redirect("cart")


def cart_view(request):
    cart = _get_cart(request)
    items = []
    subtotal = Decimal("0.00")
    for slug, qty in cart.items():
        p = get_object_or_404(Product, slug=slug)
        line = {
            "product": p,
            "qty": qty,
            "unit_price": p.price,
            "line_total": p.price * qty,
        }
        items.append(line)
        subtotal += line["line_total"]
    return render(request, "cart.html", {"items": items, "subtotal": subtotal})


# ---------- CHECKOUT & SİPARİŞLER ----------

@login_required
def checkout_view(request):
    cart = _get_cart(request)
    if not cart:
        messages.warning(request, "Sepet boş.")
        return redirect("products")

    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = Order.objects.create(user=request.user, total=0)
            total = Decimal("0.00")
            for slug, qty in cart.items():
                p = get_object_or_404(Product, slug=slug)
                OrderItem.objects.create(
                    order=order, product=p, quantity=qty, unit_price=p.price
                )
                total += p.price * qty
            order.total = total
            order.save()
            _save_cart(request, {})
            messages.success(request, "Siparişiniz oluşturuldu!")
            return redirect("orders")
    else:
        form = CheckoutForm()
    return render(request, "checkout.html", {"form": form})


@login_required
def orders_view(request):
    orders = (
        Order.objects.filter(user=request.user)
        .order_by("-created_at")
        .prefetch_related("items__product")
    )
    return render(request, "orders.html", {"orders": orders})


# ---------- KAYIT ----------

def signup_view(request):
    if request.user.is_authenticated:
        return redirect("home")

    # Kullanıcının dönmek istediği URL (örn. /shop/checkout/)
    next_url = request.GET.get("next") or request.POST.get("next") or ""

    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data["password1"]
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            # Kayıt sonrası geldigi sayfaya dön; yoksa home'a git
            return redirect(next_url or "home")
    else:
        form = SignUpForm()

    return render(request, "signup.html", {"form": form, "next": next_url})
