
from decimal import Decimal
from store.models import Product
from django.db.models import F



class Cart():

    def __init__(self,request):
        self.session=request.session  
        
        if request.user.is_authenticated:
            
             cart=self.session.get('session_lkey')
             if not cart:
                cart=self.session['session_lkey']={}
        else:
            cart=self.session.get('session_key')
            if not cart:
                cart=self.session['session_key']={}
            
        self.cart=cart
        

    def cartDict(self,request):
        self.session=request.session  
        
        if request.user.is_authenticated:
             cart=self.session.get('session_lkey')
             if not cart:
                cart=self.session['session_lkey']={}
        else:
            cart=self.session.get('session_key')
            if not cart:
                cart=self.session['session_key']={}
        
        return cart


    def save(self):
        self.session.modified = True


    def clear(self):
        for product_id in list(self.cart):
            del self.cart[product_id]

        self.save()


    def add(self,product,qty):
        product_id=str(product.id)
        if qty <= 10:
            if product_id  in self.cart:
                self.cart[product_id]['qty'] = qty
                
            else:
                self.cart[product_id] = {'price':str(product.price),'qty':qty}
        else:
             raise ValueError('Order item quantity can not be higher than 10')
        self.save()


    def reserveProductQuantity(self,product,qty):
        product_id=str(product.id)
        if qty <= 10:
            if product_id  in self.cart:
                
                try:
                    product.reservedQuantity = F('reservedQuantity') - int(self.cart[product_id]['qty'])
                    product.save(update_fields=['reservedQuantity'])
                    # product.refresh_from_db() 
                    product.reservedQuantity = F('reservedQuantity') + qty
                    product.save(update_fields=['reservedQuantity'])
                    # product.refresh_from_db() 
                except:
                    raise ValueError('Order item quantity value violates the reserved quantity constraint') 
            else:
                product.reservedQuantity = F('reservedQuantity') + qty
                product.save(update_fields=['reservedQuantity'])
                # product.refresh_from_db() 
        else:
            raise ValueError('Order item quantity can not be higher than 10')

    
    def get_cart_keys(self):
        product_ids=self.cart.keys()

        return product_ids


    def get_cart_values(self):
        values=self.cart.values()

        return values


    def get_cart_items(self):

        for item in self.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item


    def __iter__(self):

        product_ids=self.cart.keys()
        products=Product.objects.filter(id__in=product_ids)
        cart=self.cart.copy()
        

        for product in products:
            product_id=str(product.id)
            cart[str(product.id)]['product_id'] = product.id
            cart[str(product.id)]['product_imageUrl'] = product.imageUrl
            cart[str(product.id)]['product_name'] = product.name
            cart[str(product.id)]['product_availableItems'] = product.availableQuantity
            
            if (product.availableQuantity + self.cart[product_id]['qty']) > 10:
                cart[str(product.id)]['product_maxQuantity'] = 10
            else:
                 cart[str(product.id)]['product_maxQuantity'] = product.availableQuantity + self.cart[product_id]['qty']
            
            cart[str(product.id)]['product_slug'] = product.slug

        for item in cart.values():
            item['price'] = float(item['price'])
            itemTotalPrice=item['price'] * item['qty']
           
            item['total_price'] = itemTotalPrice
            yield item
            

    def __len__(self):
        return sum(item['qty'] for item in self.cart.values())


    def cart_items_quantity(self):
        return sum(item['qty'] for item in self.cart.values())


    def get_total_price(self):
        return round(sum(Decimal(item['price']) * item['qty'] for item in self.cart.values()),2)
   
    
    def delete(self,productId):
        product_id=str(productId)
        
        if product_id in self.cart:
            del self.cart[product_id]
        
        self.save()


    def get_product(self,productId):
        product_id=str(productId)

        if product_id in self.cart:
            return self.cart[product_id]
        else:
            pass


    def get_product_price(self,productId):

        product_id=str(productId)
        product_price=self.cart[product_id]['price']

        return round(float(product_price),2)


    def get_product_quantity(self,productId):

        product_id=str(productId)
        
        if product_id in self.cart:
            product_quantity=self.cart[product_id]['qty']
        else:
            product_quantity=0
        
        return product_quantity


    def reserveUpdatedProductQuantity(self,product,qty):
        product_id=str(product.id)
        
        if product_id  in self.cart:
            try:
                product.reservedQuantity = F('reservedQuantity') - int(self.cart[product_id]['qty'])
                product.save(update_fields=['reservedQuantity'])
                # product.refresh_from_db() 

                product.reservedQuantity = F('reservedQuantity') + qty
                product.save(update_fields=['reservedQuantity'])
                # product.refresh_from_db() 

            except:
                
                raise ValueError('Order item quantity value violates the reserved quantity constraint')
        else:
            product.reservedQuantity = F('reservedQuantity') + qty
            product.save(update_fields=['reservedQuantity'])
            # product.refresh_from_db() 
                
        

    def update(self,productId,qty):
        product_id=str(productId)

        if product_id in self.cart:
            self.cart[product_id]['qty']=qty
           
        self.save()



    def shipping(self):
        shipping = False

        product_ids=list(self.cart.keys())
        cartItemsTypes=Product.objects.filter(id__in=product_ids).values_list('digital',flat=True)
        for type in cartItemsTypes:
            if type == False:
                shipping=True
        return shipping

