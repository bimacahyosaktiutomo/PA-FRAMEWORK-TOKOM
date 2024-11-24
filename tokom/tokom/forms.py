from django import forms
from .models import Item, Category
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
        # widgets = {
        #     'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter item name'}),
        #     'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter item description'}),
        #     'category': forms.Select(attrs={'class': 'form-select'}),
        #     'rating': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter item rating (optional)'}),
        #     'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter stock quantity'}),
        #     'discount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter discount (optional)'}),
        #     'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price'}),
        #     'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder': 'Enter image URL (optional)'}),
        # }
        # labels = {
        #     'name': 'Item Name',
        #     'description': 'Description',
        #     'category': 'Category',
        #     'rating': 'Rating',
        #     'stock': 'Stock',
        #     'discount': 'Discount',
        #     'price': 'Price',
        #     'image': 'Image URL',
        # }

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
