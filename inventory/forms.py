from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, SetPasswordForm
from .models import Item, Currency, Sale

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'description', 'quantity', 'unit_price', 'category', 'currency', 'expiry_date']  # Removed 'price'
        widgets = {
            'currency': forms.Select(),
            'expiry_date': forms.DateInput(attrs={'type': 'date'})
        }

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['item', 'quantity']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Customize the item field to show descriptions
        self.fields['item'].queryset = Item.objects.filter(is_deleted=False).order_by('description')
        self.fields['item'].widget = forms.Select(choices=[(item.id, item.description) for item in self.fields['item'].queryset])

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=254, widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label="Email", max_length=254, widget=forms.EmailInput(attrs={'autofocus': True}))

class CustomSetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label='New password', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))
    new_password2 = forms.CharField(label='Confirm new password', widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}))