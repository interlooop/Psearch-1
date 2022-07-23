from . models import *
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from django.db.models import Q,F
from cart.cart import Cart
from django.shortcuts import get_object_or_404


def userOrder(request,data):

    cart=Cart(request)
    
    cartItemsValuesList=list(cart.get_cart_values())
    
    try:
        user=request.user
        customer,created=Customer.objects.get_or_create(
            user=user,
        )
    except:
        print('Can not get or create customer')
    
    
    product_ids=list(cart.get_cart_keys())
    
    products=[]
    for id in product_ids:
        product=get_object_or_404(Product,id=id)
        products.append(product)

    
    if 'orderId' in request.session:
            orderId = request.session['orderId']

            order,created=Order.objects.get_or_create(
                id=orderId,
                customer=customer,
                complete=False,
            )
    else:
            order,created=Order.objects.get_or_create(
                customer=customer,
                complete=False,
            )

    
    count=0
    for product in products:
        orderItem,created=OrderItem.objects.get_or_create(
            product=product,
            order=order,
        )
        orderItem.quantity=cartItemsValuesList[count]['qty']
        orderItem.save(update_fields=['quantity'])
        count+=1
        
        try:
                product.qtyInStock = F('qtyInStock') - orderItem.quantity
                product.reservedQuantity = F('reservedQuantity') - orderItem.quantity
                product.save(update_fields=['qtyInStock','reservedQuantity'])
        except:
                print('Order item quantity can not be higher than the available quantity')

    return customer, order



def paginateProducts(request, products,results):
    
    
    page=request.GET.get('page')
    
    
    paginator=Paginator(products, results)

    try:
       products=paginator.page(page)
    except PageNotAnInteger:
        page=1
        products=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        products=paginator.page(page)

    
    leftIndex=(int(page)-4)
    if leftIndex<1:
        leftIndex=1

    rightIndex=(int(page)+5)
    if rightIndex>paginator.num_pages:
        rightIndex=paginator.num_pages+1

    custom_range=range(leftIndex,rightIndex)

    return custom_range, products



def searchProducts(request,search_query,category=None):

    if search_query == None:
        search_query=''


    if category:
        products=Product.objects.distinct().filter(
        Q(name__icontains=search_query),
        category=category)
    else:
        products=Product.objects.distinct().filter(
            Q(name__icontains=search_query)
        )

    return products,search_query

