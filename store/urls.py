from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('product/<int:id>/',views.product_details,name='product_detail'),
    path('cart/',views.cart,name='cart'),
    path('add-to-cart/<int:id>/',views.add_to_cart,name='add_to_cart'),
    path('cart/increase/<int:item_id>/',views.increase_quantity,name='increase_quantity'),
    path('cart/decrease/<int:item_id>/',views.decrease_quantity,name='decrease_quantity'),
    path('cart/remove/<int:item_id>/',views.remove_from_cart,name='remove_from_cart'),

    # les urls pour l'inscription, la connexion et la deconnexion
    path('register/',views.register,name='register'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),

    # Urls pour effectuer une commande
    path('checkout/',views.checkout,name='checkout'),

    # urls pour consulter ses commandes
    path('my-orders/',views.my_orders,name='my_orders'),

    ## urls pour consulter les produits de sa commande
    path('order/<int:order_id>/',views.order_detail,name='order_detail'),

    ## urls pour les produits
    path('products/',views.products,name='products'),

    ## urls pour toutes les categories
    path('categories/',views.categories,name='categories'),
    path('category/<int:id>/',views.category_products,name='category_products'),

    ## urls pour les profiles utilisateurs
    path('profile/',views.profile,name='profile')
]