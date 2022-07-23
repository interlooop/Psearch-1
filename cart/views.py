# from asyncio.windows_events import NULL
from django.shortcuts import render,get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import *
from django.core.exceptions import ValidationError
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.template.loader import render_to_string
from django.db import transaction

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class cart_summaryView(LoginRequiredMixin,View):
    
    def get(self, request):

            if request.session.get('continue') == None:
                request.session['continue'] = True
            cart=Cart(request)
            cartItems=cart.cart_items_quantity()

            context={'cart':cart,'cartItems':cartItems}
            return render(request,'store/cart.html',context)



class cart_addView(LoginRequiredMixin,View):
    
    def post(self, request):
        
        cart=Cart(request)
        data = {
                'msg': render_to_string('messages.html', {}),
                }

        productId=int(request.POST.get('productId'))

        try:
            product_qty=int(request.POST.get('productQty'))
        except ValueError:
            msg='Please specify correct ammount'
            messages.add_message(request, messages.ERROR, msg)
            return JsonResponse({'data':data})
            
        with transaction.atomic():
            product = Product.objects.select_for_update(nowait=True).get(id=productId)
            
            cartProductQuantity=cart.get_product_quantity(product.id)

            if cartProductQuantity + product.availableQuantity > 10:
                maxQuantity=10
            else:
                maxQuantity=cartProductQuantity + product.availableQuantity
                

            try:
                if product_qty <= 10 and product_qty <= maxQuantity and product_qty > 0:
                    cart.reserveProductQuantity(product=product,qty=product_qty)
                    cart.add(product=product,qty=product_qty)
                    messages.add_message(request, messages.SUCCESS, "Item added to cart")
                else:
                    raise ValueError('Ordered amount is not available')
            except ValueError as ve:
                msg=str(ve)
                messages.add_message(request, messages.WARNING, msg)
                    
                return JsonResponse({'data':data})


        cart_qty=cart.__len__()
       
        
               
        user=request.user
        customer,created=Customer.objects.get_or_create(
            user=user,
        )
                
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
                
        orderItem.quantity=product_qty
        orderItem.save(update_fields=['quantity'])

        response = JsonResponse({'qty':cart_qty})

        return response




   
class cart_deleteView(LoginRequiredMixin,View):
    def post(self,request):
        cart=Cart(request)
        product_id=int(request.POST.get('productId'))
        
        
        if request.POST.get('action') == 'post':
            action2=request.POST.get('action2')
            
            cartItemQuantity=cart.get_product_quantity(product_id)    
            cart.delete(productId=product_id)
            if cart.__len__():
                cart_qty=cart.__len__()
            else:
                cart_qty="0"
            cart_total_price=cart.get_total_price()


            user=request.user
            customer,created=Customer.objects.get_or_create(
                user=user,
            )
                
            order,created=Order.objects.get_or_create(customer=customer,complete=False)
            
            with transaction.atomic():
                product = Product.objects.select_for_update(nowait=True).get(id=product_id)
            
                orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
                    
                if action2 == "remove":
                    product.reservedQuantity-=cartItemQuantity
                    product.save(update_fields=['reservedQuantity'])
                    orderItem.quantity=0
                    orderItem.save(update_fields=['quantity'])
                    orderItem.delete()


            response =JsonResponse({'cart_qty':cart_qty,'cart_total_price':cart_total_price})
            return response




class cart_updateView(LoginRequiredMixin,View):
    def post(self,request):
        cart=Cart(request)
        data = {
                'msg': render_to_string('messages.html', {}),
                }

        if request.POST.get('action') == 'post':
            
            product_id=int(request.POST.get('productId'))
            
            try:
                product_qty=int(request.POST.get('productQty'))
            except ValueError:
                msg='Please specify correct ammount'
                messages.add_message(request, messages.ERROR, msg)
                return JsonResponse({'data':data})

            product_qty_max=int(request.POST.get('productQty'))
            product=get_object_or_404(Product, id=product_id)
            
            try:
                cartProductQty=cart.get_product_quantity(product.id)

                if product_qty <= 10 and product_qty > 0 and product_qty <= product.availableQuantity + cartProductQty:   
                    cart.reserveUpdatedProductQuantity(product=product,qty=product_qty)
                    cart.update(productId=product_id,qty=product_qty)
                else:
                        request.session['continue']=False
                        raise ValueError('Ordered quantity for ' + product.name + ' can not be higher than 10, higher than the remaining available quantity or lower than 1, please correct your order quantity if you want to proceed')
                
            except ValueError as ve:
                    msg=str(ve)
                    messages.add_message(request, messages.ERROR, msg)
                        
                    return JsonResponse({'data':data})
            

            if request.user.is_authenticated:
               
                user=request.user
                customer,created=Customer.objects.get_or_create(
                    user=user,   
                )
                
                order,created=Order.objects.get_or_create(customer=customer,complete=False)
                orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
               
                orderItem.quantity=product_qty
                orderItem.save(update_fields=['quantity'])


            product_price=cart.get_product_price(productId=product_id)

            product_total_price=product_qty * product_price
                
            cart_qty=cart.__len__()
            cart_total_price=cart.get_total_price()


            response=JsonResponse({'cart_qty':cart_qty,'cart_total_price':cart_total_price,'product_total_price':round(product_total_price,2)})
            return response











