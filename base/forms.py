from django import forms
from .models import Comment, Listing, Review
from base.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.admin import UserAdmin
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write a comment...'}),
        }
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'profile_pic']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_pic': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.lower().endswith('@charlotte.edu'):
            raise forms.ValidationError('Email must end with "@charlotte.edu"')
        return email
    
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'password1': 'Password',
            'password2': 'Confirm Password',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),      
        }

    def clean(self):
        cleaned_data = super().clean()

        # Rename 'password2' field errors to show as 'Password'
        if 'password2' in self._errors:
            self._errors['Confirm Password'] = self._errors.pop('password2')
        
        return cleaned_data

from django import forms
from .models import Listing

class ListingForm(forms.ModelForm):
    accepted_payments = forms.MultipleChoiceField(
        choices=Listing.PAYMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    negotiable = forms.ChoiceField(
        choices=[
            (True, 'Yes'),
            (False, 'No')
        ],
        widget=forms.RadioSelect
    )

    condition = forms.ChoiceField(
        choices=Listing.CONDITION_CHOICES,
        widget=forms.RadioSelect
    )
    
    CATEGORY_CHOICES = [
            ('Electronics', 'Electronics'),
            ('Sports', 'Sports'),
            ('Clothing', 'Clothing'),
            ('Books', 'Books'),
            ('Furniture', 'Furniture'),
            ('Other', 'Other')
        ]
    
    category = forms.ChoiceField(
            choices=CATEGORY_CHOICES,
            widget=forms.Select(attrs={'class': 'form-control'})
        )

    class Meta:
        model = Listing
        
        fields = [
            'title',
            'description',
            'price',
            'quantity',
            'accepted_payments',
            'negotiable',
            'condition',
            'category',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your review here...'})
        }