from .models import Cart

def cart_counter(request):

    count = 0

    if request.user.is_authenticated:

        cart, created = Cart.objects.get_or_create(
            user=request.user
        )

        count = sum(
            item.quantity
            for item in cart.items.all()
        )

    return {
        'cart_count': count
    }