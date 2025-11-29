class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get("cart")
        if not cart:
            cart = self.session["cart"] = {}
        self.cart = cart
    def add(self, product , product_quantity):
        product_id = str(product.id) 
        if product_id in self.cart :
            self.cart[product_id]["qtty"] += product_quantity
        else:
            self.cart[product_id] = {"price": product.price , "qtty" : product_quantity}
        self.save()
    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True
