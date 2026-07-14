from django.shortcuts import render,  get_object_or_404, redirect
from .models import Category, Product, Cart, CartItem, User,  Order, OrderItem
from django.contrib.auth.decorators import login_required # pour proteger mes vues
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator

# vue pour la page d'accueil et la barre de recherche des produits
def home(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    return render(
        request,
        'home.html',
        {
            'products': products,
            'categories': categories,
        }
    )

## vue pour la page produits
def products(request):

    query = request.GET.get('q')
    category_id = request.GET.get('category')

    products = Product.objects.all()
    categories = Category.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    if category_id:
        products = products.filter(
            category_id=category_id
        )

    paginator = Paginator(products, 8)

    page_number = request.GET.get('page')

    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'selected_category': category_id
    }

    return render(
        request,
        'products1.html',
        context
    )
## vue pour les categories
def categories(request):

    categories = Category.objects.all()

    return render(
        request,
        'categories.html',
        {
            'categories': categories
        }
    )

## vue les produits d'une categorie
def category_products(request, id):

    category = Category.objects.get(id=id)

    products = Product.objects.filter(
        category=category
    )

    return render(
        request,
        'category_products.html',
        {
            'category': category,
            'products': products
        }
    )

def product_details(request, id):

    product = get_object_or_404(
        Product,
        id=id
    )

    return render(
        request,
        'product_details.html',
        {
            'product': product
        }
    )


#@login_required l'utilisateur doit etre connecter avant de pourvoir ajouter des elements au painer
@login_required(login_url='login')
def cart(request):

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    total = 0

    for item in cart.items.all():
        total += item.subtotal()

    context = {
        'cart': cart,
        'total': total
    }

    return render(
        request,
        'cart.html',
        context
    )

@login_required(login_url='login')
# pour l'ajout d'un ou plusieurs elements au panier
@login_required(login_url='login')
def add_to_cart(request, id):

    product = Product.objects.get(id=id)

    # Vérifier le stock
    if product.stock <= 0:

        messages.error(
            request,
            "Ce produit est en rupture de stock."
        )

        return redirect(
            'product_detail',
            id=product.id
        )

    cart, created = Cart.objects.get_or_create(
        user=request.user
    )

    item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        item.quantity += 1
        item.save()

    messages.success(
        request,
        f"{product.name} a été ajouté au panier."
    )

    return redirect('cart')

# vue pour ajouter la quantité d'un produit
#@login_required
@login_required(login_url='login')
def increase_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    item.quantity += 1
    item.save()

    return redirect('cart')

# vue pour diminuer la quantité d'un produit
# @login_required
@login_required(login_url='login')
def decrease_quantity(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    if item.quantity > 1:

        item.quantity -= 1

        item.save()

    return redirect('cart')

# vue pour supprimer un element du panier
#@login_required
@login_required(login_url='login')
@login_required(login_url='login')
def remove_from_cart(request, item_id):

    item = get_object_or_404(
        CartItem,
        id=item_id
    )

    product_name = item.product.name

    item.delete()

    messages.success(
        request,
        f"{product_name} supprimé du panier."
    )

    return redirect('cart')

## vue pour la creation de compte
def register(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(
                request,
                "Les mots de passe ne correspondent pas."
            )
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(
                request,
                "Cet email existe déjà."
            )
            return redirect('register')

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )

        messages.success(
            request,
            "Compte créé avec succès."
        )

        return redirect('login')

    return render(request, 'register.html')

# vue pour se connecter
def login_view(request):

    if request.method == "POST":

        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=email,
            password=password
        )
        next_url = request.GET.get('next')

        if user is not None:
            user.password
            login(request, user)

            messages.success(
                request,
                "Connexion réussie."
            )

            if next_url:
                return redirect(next_url)

            return redirect('home')
        messages.error(
            request,
            "Email ou mot de passe incorrect."
        )


    return render(
        request,
        'login.html'
    )

## vue pour se deconnecter
def logout_view(request):
    logout(request)

    messages.success(
        request,
        "Déconnexion réussie."
    )

    return redirect('home')

## vue pour les commandes
@login_required(login_url='login')
def checkout(request):

    cart = Cart.objects.get(
        user=request.user
    )

    cart_items = cart.items.all()

    if not cart_items:
        return redirect('cart')

    total = 0

    order = Order.objects.create(
        user=request.user
    )

    for item in cart_items:

        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.price
        )

        total += item.product.price * item.quantity

        # mise à jour du stock
        item.product.stock -= item.quantity
        item.product.save()

    order.total = total
    order.save()

    # vider le panier
    cart_items.delete()

    messages.success(
        request,
        f"Votre commande N°{order.id} a été enregistrée avec succès."
    )

    return render(
        request,
        'home.html',
        {
            'order': order
        }
    )

## vue pour les commandes pour consulter ses commandes
@login_required(login_url='login')
def my_orders(request):

    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'my_orders1.html',
        {
            'orders': orders
        }
    )

## vue pour la consultation des produits d'une commande
@login_required(login_url='login')
def order_detail(request, order_id):

    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'order_detail.html',
        {
            'order': order
        }
    )

## vue le profile utilisateur
@login_required(login_url='login')
def profile(request):

    orders_count = Order.objects.filter(
        user=request.user
    ).count()

    return render(
        request,
        'profile.html',
        {
            'orders_count': orders_count
        }
    )

