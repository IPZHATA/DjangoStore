from cart.service import CartService


#це нада, шоб на base сторінці відображати к-сть товарів з корзини
def cart_size(request):
    current_user = request.user
    cart_size = len(CartService.get_or_create_cart(current_user).items.all())
    return {'cart_size': cart_size}