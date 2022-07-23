
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout

from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.contrib.auth.models import User

from store.models import Order, OrderItem, Product

from .models import Profile,Social
from django.views import View
from .forms import CustomUserCreationForm, ProfileForm, SkillForm, ProfileSocialForm,MessageForm, GuestMessageForm
from .utils import paginate, searchProfiles, token_generator

from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from cart.cart import Cart

import threading
import datetime

class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()


# Create your views here.
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class LoginUserView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('profiles')

        return render(request, 'users/login-register.html')
        

    def post(self, request):
        username=request.POST['username'].lower()
        password=request.POST['password']
 
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')

        user=authenticate(request, username=username, password=password)

        if user is not None:
            
            request.session.pop('session_key')
            login(request, user)
            request.session.set_expiry(900)

            try:
                cart=Cart(request)
                customer=request.user.customer
                
                order=get_object_or_404(Order,customer=customer,complete=False)
                orderItems=order.orderitem_set.all()
                for item in orderItems:
                    product=Product.objects.get(name=item.product.name)
                    quantity=item.quantity
                    cart.add(product=product,qty=quantity)
                
            except:
                pass

            return redirect(request.GET['next'] if 'next' in request.GET else 'account')
        else:
            messages.error(request,'Username OR password is incorrect!')   
            return render(request, 'users/login-register.html')
            


class LogoutUserView(View):
    
    def get(self, request):
        if 'session_lkey' in request.session:
            cart=Cart(request)
            
            cartItemsValuesList=list(cart.get_cart_values())
            try:
                customer=request.user.customer 

                product_ids=list(cart.get_cart_keys())
                products=[]
                for id in product_ids:
                    product=get_object_or_404(Product,id=id)
                    products.append(product)
                
                if 'orderId' in request.session:
                    orderId = request.session['orderId']
                    try:
                        order=get_object_or_404(Order,
                            id=orderId,
                            customer=customer,
                            complete=False,
                        )
                    except:
                        pass
                else:
                    try:
                        order=get_object_or_404(Order,
                            customer=customer,
                            complete=False,
                        )
                    except:
                        pass
                order.save()

                count=0
                for product in products:
                    orderItem,created=OrderItem.objects.get_or_create(
                        product=product,
                        order=order,
                    )
                    quantity=cartItemsValuesList[count]['qty']
                    orderItem.quantity=quantity
                    orderItem.save(update_fields=['quantity'])
                    count+=1
            except:
                pass

        logout(request)
        
        messages.info(request,'User was logged out!')
        return redirect('login-user')
        

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class RegisterUserView(View):
    def get(self, request):
        page='register'
        form=CustomUserCreationForm()  

        context={'page':page,'form':form}
        
        return render(request, 'users/login-register.html',context)

    def post(self, request):
        page='register'
        form=CustomUserCreationForm(request.POST)

        context={'page':page,'form':form}
        
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.is_active=False
            user.id=datetime.datetime.now().timestamp()
            user.save()
            

            uidb64=urlsafe_base64_encode(force_bytes(user.id))
    
            domain=get_current_site(request).domain
            link=reverse('activate',kwargs={'uidb64':uidb64,'token':token_generator.make_token(user)})

            
            activation_url='http://'+domain+link

            email_subject='Activate Your psearch account in order to proceed'
            email_body='Hello '+user.username+', please use this link in order to verify your psearch account\n'+ activation_url
            
            try:
                send_mail(
                    email_subject,
                    email_body,
                    settings.EMAIL_HOST_USER,
                    [form.cleaned_data['email']],
                    fail_silently=False,
                )
                
                return redirect('activation-successful')
            except:
                messages.error(request,'An error has occurred during registration! Check if the email address You have entered is correct!')
                return render(request, 'users/login-register.html',context)
                
        else:
            messages.error(request,'An error has occurred during registration!')
            return render(request, 'users/login-register.html',context)



class VerificationView(View):
    def get(self, request, uidb64, token):
        
        try:
            id=force_text(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=id)
            

            if not token_generator.check_token(user,token):
                return redirect('login-user'+'?message='+'User already activated')

            if user.is_active:
                return redirect('login-user')
            user.is_active=True
            user.save()

            messages.success(request,'Account activated succesfully')
            return redirect('login-user')

        except Exception as ex:
            pass


        return redirect('login-user')



class ActivationSuccessfulView(View):
    def get(self,request):
        return render(request,'users/activation-successful.html')



class ProfilesView(View):
    def get(self, request):
        searchValue=''
        profiles,search_query=searchProfiles(request,searchValue)
        
    
        custom_range,profiles=paginate(request,profiles,6)

        context = {'profiles': profiles,'search_query':search_query,
                    'custom_range':custom_range}
                    
        return render (request, 'users/profiles.html', context)


class FilteredProfilesView(View):
   
    def get(self, request):
        searchValue=request.GET.get('searchValue')
        profiles,search_query=searchProfiles(request,searchValue)
        
        custom_range,profiles=paginate(request,profiles,6)

    
        context = {'profiles': profiles, 'custom_range':custom_range}
                    
        return render (request, 'users/filtered-profiles.html', context)



class UserProfileView(View):
    def get(self, request,pk):
        try:
            profile=Profile.objects.get(id=pk)
            social,created=Social.objects.get_or_create(owner=profile)

            skillsWithDesc=profile.skill_set.exclude(description__exact="")
            skillsNoDesc=profile.skill_set.filter(description="")
        except:
            messages.error(request,"An error has occured")
            return redirect('profiles')
        

        context={'profile': profile,'social':social,'skillsWithDesc':skillsWithDesc, 'skillsNoDesc': skillsNoDesc }
        
        return render(request,'users/user-profile.html', context)



@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class UserAccountView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        profile=request.user.profile
        social,created=Social.objects.get_or_create(owner=profile)

        skills=profile.skill_set.all()
        projects=profile.project_set.all()
        custom_range,projects=paginate(request,projects,2)
        
        context={'profile':profile,'skills':skills, 'projects':projects, 'social':social,'custom_range':custom_range}
       
        return render(request,'users/account.html', context)


@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class PaginatedUserProjectsView(LoginRequiredMixin,View):
   
    def get(self, request):
        profile=request.user.profile
        projects=profile.project_set.all()
        
        custom_range,projects=paginate(request,projects,2)

    
        context = {'projects':projects,'custom_range':custom_range}
                    
        return render (request, 'users/paginated-user-projects.html', context)



@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class EditAccountView(LoginRequiredMixin,View):
    def get(self, request):
        profile=request.user.profile
        social,created=Social.objects.get_or_create(owner=profile)


        form=ProfileForm(instance=profile)
        form_social=ProfileSocialForm(instance=social)

        context={'form':form,'form_social':form_social}
        
        return render(request, 'users/profile-form.html',context)


    def post(self, request):    
        profile=request.user.profile
        social,created=Social.objects.get_or_create(owner=profile)


        if request.method=='POST':
            form=ProfileForm(request.POST, request.FILES,instance=profile)
            form_social=ProfileSocialForm(request.POST,instance=social)
            
            if form.is_valid() and form_social.is_valid():
                
                    form.save()
                    form_social.save()

                    return redirect('account')
                
            else:
                context={'form':form,'form_social':form_social}
        
                return render(request, 'users/profile-form.html',context)
           


@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class CreateSkillView(LoginRequiredMixin,View):
    
    def get(self, request):
        form=SkillForm()

        context={'form':form}
        return render(request,'users/skill-form.html',context)


    def post(self, request):
        profile=request.user.profile 
        
        if request.method=='POST':
            form=SkillForm(request.POST)
            if form.is_valid():
                try:
                    skill=form.save(commit=False)
                    skill.owner=profile
                    skill.save(update_fields=['owner'])
                    messages.success(request, 'Skill was added successfully!')

                    return redirect('account')
                except:
                    messages.error(request,'An error has occurred!')
                    return redirect('create-skill')

   

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class UpdateSkillView(LoginRequiredMixin,View):
    def get(self, request,pk):
        try:
            profile=request.user.profile
            skill=profile.skill_set.get(id=pk)
            form=SkillForm(instance=skill)

            context={'form':form}
            return render(request,'users/skill-form.html',context)

        except:
            messages.error(request,'An error has occurred!')
            return redirect('account')


    def post(self, request,pk):
        profile=request.user.profile
        skill=profile.skill_set.get(id=pk)

        if request.method=='POST':
            form=SkillForm(request.POST,instance=skill)
            if form.is_valid():
                try:
                    form.save()
                    messages.success(request, 'Skill was updated successfully!')

                    return redirect('account')
                except:
                    messages.error(request,'An error has occurred!')
                    return redirect('update-skill')

    

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class DeleteSkillView(LoginRequiredMixin,View):
    
    def get(self, request,pk):
        try:
            profile=request.user.profile
            skill=profile.skill_set.get(id=pk)

            context={'object': skill}
        except:
            messages.error(request,'An error has occurred!')
            return redirect('account')

        return render(request,'delete-template.html',context)
    

    def post(self, request,pk):
        if request.method=='POST':
            profile=request.user.profile
            skill=profile.skill_set.get(id=pk)
            
            try:
                skill.delete()
                messages.success(request, 'Skill was deleted successfully!')
                return redirect('account')
            except:
                messages.error(request,'An error has occurred!')
                return redirect('delete-skill')

    

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class InboxView(LoginRequiredMixin,View):
    def get(self, request):
        profile=request.user.profile
        messageRequests=profile.messages.all()
        totalMessages=messageRequests.count()
        custom_range,messageRequests=paginate(request,messageRequests,3)

    
        context={'messageRequests':messageRequests,'custom_range':custom_range,'totalMessages':totalMessages}
        
    
        return render(request,'users/inbox.html',context)



@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class PaginatedInboxView(LoginRequiredMixin,View):
    
    def get(self, request):
        
        profile=request.user.profile
        messageRequests=profile.messages.all()
        totalMessages=messageRequests.count()
        custom_range,messageRequests=paginate(request,messageRequests,3)

        
        context = {'messageRequests': messageRequests,'custom_range':custom_range,'totalMessages':totalMessages}
                    
        return render (request, 'users/paginated-inbox.html', context)



@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class ViewMessageView(LoginRequiredMixin,View):
    def get(self, request,pk):
        profile=request.user.profile
        message=profile.messages.get(id=pk)
        
        if message.is_read==False:
            message.is_read=True
            message.save(update_fields=['is_read'])

        context={'message':message}
        
        return render(request,'users/message.html',context)



@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class CreateMessageView(View):

    def get(self,request,pk):
        try:
            recipientId=Profile.objects.filter(id=pk).values('id')
        except:
            messages.error(request,"An error has occured")
            return redirect('profiles')
        
        if request.user.is_authenticated:
            form=MessageForm()
        else:
            form=GuestMessageForm()    
        
        context={'recipientId': recipientId,'form':form}
        return render(request,'users/message-form.html',context)

       

    def post(self,request,pk):
        try:
            recipient=Profile.objects.get(id=pk)
        except:
            messages.error(request,"An error has occured")
            return redirect('profiles')

        try:
            sender=request.user.profile
        except:
            sender=None

        if request.method == 'POST':
            if request.user.is_authenticated:
                form=MessageForm(request.POST)
            else:
                form=GuestMessageForm(request.POST)
            
            
            if form.is_valid():
    
                message=form.save(commit=False)
        
                message.sender=sender
                message.recipient=recipient

                if sender:
                    message.name=sender.name
                    message.email=sender.email
                message.save(update_fields=['sender','recipient','name','email'])

                messages.success(request,'Your message was successfully sent!')

                return redirect('user-profile', pk=recipient.id)
            else:
                messages.error(request,'An error has occurred! Check the email you have entered is correct!')
                return redirect('create-message',pk=pk)

        
        
        
@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='get')
class DeleteMessageView(LoginRequiredMixin ,View):

    def get(self, request,pk):
        try:
            profile=request.user.profile
            message=profile.messages.get(id=pk)

            context={'object': message}
        except:
            messages.error(request,'An error has occurred!')
            return redirect('inbox')

        return render(request,'delete-template.html',context)
   

    def post(self, request,pk):
        if request.method=='POST':
            profile=request.user.profile
            message=profile.messages.get(id=pk)
            try:
                message.delete()
                messages.success(request, 'Message was deleted successfully!')
                return redirect('inbox')
            except:
                messages.error(request,'An error has occurred!')
                return redirect('delete-message')

