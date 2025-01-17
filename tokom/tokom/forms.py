from django import forms
from .models import Item, Category, Review
from .models.user_image import UserImage
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.core.exceptions import ValidationError

class ItemForm(forms.ModelForm):
    new_category = forms.CharField(
        max_length=40,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter new category (optional)'}),
        label="New Category",
    )

    class Meta:
        model = Item
        fields = ['name', 'description', 'category', 'rating', 'stock', 'discount', 'price', 'image']

    def clean(self):
        """
        Additional cross-field validation for `category` and `new_category`.
        """
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        new_category = cleaned_data.get('new_category')

        if not category and not new_category:
            # Automatically assign the first category as a default
            category = Category.objects.first()
            if not category:
                raise forms.ValidationError("No categories available to assign. Please add a category first.")
            cleaned_data['category'] = category

        if new_category:
            # Create or get a new category and set it as the `category` for the item
            category, created = Category.objects.get_or_create(name=new_category)
            cleaned_data['category'] = category

        return cleaned_data

class UserForm(UserChangeForm):
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'file-input file-input-bordered w-full max-w-xs'})
    )

    password = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            # 'class': 'mt-1 block w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-blue-500 focus:outline-none',
        }),
        label="Password",
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name', 'is_staff', 'is_active']

    def save(self, commit=True):
        user = super().save(commit=False)  # Save the base User fields
        if commit:
            user.save()
            # Save or update the UserImage model instance
            image = self.cleaned_data.get('image')
            if image:
                UserImage.objects.update_or_create(
                    user=user,
                    defaults={'image': image},
                )
        return user

class UserProfileForm(UserChangeForm):
    # Add the image field manually
    image = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(),
        allow_empty_file=True,
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def save(self, commit=True):
        user = super().save(commit=False)  # Save the base User fields
        if commit:
            user.save()
            # Save or update the UserImage model instance
            image = self.cleaned_data.get('image')
            if image:
                UserImage.objects.update_or_create(
                    user=user,
                    defaults={'image': image},
                )
        return user

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]

class CartAddItemForm(forms.Form):
    """
    Form for adding items to the cart or updating their quantity.
    """
    quantity = forms.TypedChoiceField(
        choices=PRODUCT_QUANTITY_CHOICES,
        coerce=int,
        label="Quantity"
    )
    update = forms.BooleanField(
        required=False,
        initial=False,
        widget=forms.HiddenInput
    )
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['review_text', 'image', 'rating']  # Include fields you want to be editabl