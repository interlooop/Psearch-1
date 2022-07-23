from django.forms import ModelForm,CharField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Social,Skill,Message
from django.core.validators import RegexValidator

class CustomUserCreationForm(UserCreationForm):
  
    class Meta:
        model=User
        fields=['first_name', 'email','username','password1','password2']
        labels={
            'first_name':'Name',
        }



    def __init__(self, *args,**kwargs):
        super(CustomUserCreationForm, self).__init__(*args,**kwargs)
        self.fields['email'].required = True
        self.fields['first_name'].required = True



        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class ProfileForm(ModelForm):
    class Meta:
        model= Profile
        fields= ['name','email','username','location',
        'bio','experience','intro','profile_image']


    name = CharField(
        max_length=200,
        required=True,
        validators=[
           RegexValidator(
                regex=r'^[a-zA-Z\s\'\-]*$',
                message='Only alphabetic characters,- and \' are allowed for the name field.',
                code='invalid_name'
            ),
        ]
    )

    location = CharField(
        max_length=200,
        required=True,
        validators=[
           RegexValidator(
                regex=r'^[a-zA-Z\s\'\-]*$',
                message='Only alphabetic characters,- and \' are allowed for the location field.',
                code='invalid_location'
            ),
        ]
    )


    def __init__(self, *args,**kwargs):
        super(ProfileForm, self).__init__(*args,**kwargs)
        self.fields['email'].required = True
        self.fields['name'].required = True

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class ProfileSocialForm(ModelForm):
    class Meta:
        model= Social
        fields= ['social_github','social_twitter','social_linkedin','social_website']


    def __init__(self, *args,**kwargs):
        super(ProfileSocialForm, self).__init__(*args,**kwargs)

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class SkillForm(ModelForm):
    class Meta:
        model= Skill
        fields= '__all__'
        exclude=['owner']


    def __init__(self, *args,**kwargs):
        super(SkillForm, self).__init__(*args,**kwargs)
        self.fields['name'].required = True
        

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class MessageForm(ModelForm):


    class Meta:
        model=Message
        fields=['email','subject','body']

        
    def __init__(self, *args,**kwargs):
        super(MessageForm, self).__init__(*args,**kwargs)
        self.fields['email'].required = True
        self.fields['subject'].required = True
        

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})



class GuestMessageForm(ModelForm):

    class Meta:
        model=Message
        fields=['name','email','subject','body']

     
    name = CharField(
        max_length=200,
        required=True,
        validators=[
           RegexValidator(
                regex=r'^[a-zA-Z\s\'\-]*$',
                message='Only alphabetic characters,- and \' are allowed for the name field.',
                code='invalid_guest_message_form_name'
            ),
        ]
    )

    def __init__(self, *args,**kwargs):
        super(GuestMessageForm, self).__init__(*args,**kwargs)
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['subject'].required = True
        

        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
