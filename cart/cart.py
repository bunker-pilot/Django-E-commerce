from store.models import Product
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
            self.cart[product_id]["qty"] += product_quantity
        else:
            self.cart[product_id] = {"price": float(product.price) , "qty" : product_quantity}
        self.save()
    def __len__(self) :
        return sum(item["qty"] for item in self.cart.values())

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart_item  = cart[str(product.id)]
            yield {
                "product" : product,
                "qty" : cart_item["qty"],
                "price" : cart_item["price"],
                "total_price" : cart_item["qty"] * cart_item["price"],
             }

    def delete(self, product_id):
        product_id= str(product_id)

        if product_id in self.cart:
            del self.cart[product_id]
        self.save()

    def total_price(self):
        return sum(item["price"] * item["qty"] for item in self.cart.values())

    def save(self):
        self.session["cart"] = self.cart
        self.session.modified = True
