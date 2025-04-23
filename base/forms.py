from django import forms
from .models import Comment, Listing, ListingImage
from base.models import User

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

class ListingForm(forms.ModelForm):
    accepted_payments = forms.MultipleChoiceField(
        choices=Listing.PAYMENT_CHOICES,
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    negotiable = forms.ChoiceField(
        choices=[(True, 'Yes'), (False, 'No')],
        widget=forms.RadioSelect
    )
    condition = forms.ChoiceField(
        choices=Listing.CONDITION_CHOICES,
        widget=forms.RadioSelect
    )

    class Meta:
        model = Listing
        fields = ['title', 'description', 'price', 'quantity',
                  'accepted_payments', 'negotiable', 'condition']