from django import forms
from .models import ContactMessage, NewsletterSubscriber, FinancingApplication, JobApplication, TradeInRequest, RentalRequest, Review

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'message']

class NewsletterForm(forms.ModelForm):
    class Meta:
        model = NewsletterSubscriber
        fields = ['email']

class FinancingApplicationForm(forms.ModelForm):
    class Meta:
        model = FinancingApplication
        fields = [
            'full_name', 'email', 'phone', 'country', 'address',
            'employment_details', 'business_details',
            'government_id_file', 'drivers_license_file', 'proof_of_income_file'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'w-input', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'w-input', 'placeholder': 'Phone Number'}),
            'country': forms.TextInput(attrs={'class': 'w-input', 'placeholder': 'Country'}),
            'address': forms.Textarea(attrs={'class': 'w-input', 'placeholder': 'Full Address', 'rows': 2}),
            'employment_details': forms.Textarea(attrs={'class': 'w-input', 'placeholder': 'Employment Details (Company, Role, Duration)', 'rows': 3}),
            'business_details': forms.Textarea(attrs={'class': 'w-input', 'placeholder': 'Business Details (If applicable)', 'rows': 3}),
            'government_id_file': forms.FileInput(attrs={'class': 'w-input', 'accept': 'image/*,.pdf'}),
            'drivers_license_file': forms.FileInput(attrs={'class': 'w-input', 'accept': 'image/*,.pdf'}),
            'proof_of_income_file': forms.FileInput(attrs={'class': 'w-input', 'accept': 'image/*,.pdf'}),
        }

class TradeInRequestForm(forms.ModelForm):
    class Meta:
        model = TradeInRequest
        fields = [
            'full_name', 'email', 'phone', 'make', 'model', 'year', 'mileage',
            'vin', 'condition', 'interested_in', 'notes', 'pickup_address', 'photos'
        ]
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-input', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'Phone Number'}),
            'make': forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'e.g., Toyota'}),
            'model': forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'e.g., Camry'}),
            'year': forms.NumberInput(attrs={'class': 'form-input w-input', 'placeholder': 'e.g., 2018'}),
            'mileage': forms.NumberInput(attrs={'class': 'form-input w-input', 'placeholder': 'e.g., 45000'}),
            'vin': forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'Optional: 17-digit VIN'}),
            'condition': forms.Select(attrs={'class': 'form-input w-input'}),
            'interested_in': forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'Optional: What car are you looking for?'}),
            'notes': forms.Textarea(attrs={'class': 'form-input form-textarea w-input', 'placeholder': 'Optional: Any damage, issues, or recent repairs?'}),
            'pickup_address': forms.Textarea(attrs={'class': 'form-input form-textarea w-input', 'placeholder': 'Where should we pick up the vehicle?', 'rows': 2}),
            'photos': forms.FileInput(attrs={'class': 'w-input', 'style': 'padding: 10px;'}),
        }

class RentalRequestForm(forms.ModelForm):
    class Meta:
        model = RentalRequest
        fields = ['full_name', 'email', 'phone', 'delivery_address', 'start_date', 'end_date', 'special_requests']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-input w-input', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'Phone Number'}),
            'delivery_address': forms.Textarea(attrs={'class': 'form-input form-textarea w-input', 'placeholder': 'Where should we deliver the vehicle?', 'rows': 2}),
            'start_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-input w-input', 'placeholder': 'Select Date'}),
            'end_date': forms.DateInput(attrs={'type': 'text', 'class': 'form-input w-input', 'placeholder': 'Select Date'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-input form-textarea w-input', 'placeholder': 'Any special requirements or pickup instructions?'}),
        }

class CardPaymentForm(forms.Form):
    card_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'Name on Card'}))
    card_number = forms.CharField(max_length=19, widget=forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'XXXX XXXX XXXX XXXX'}))
    expiry = forms.CharField(max_length=5, widget=forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'MM/YY'}))
    cvv = forms.CharField(max_length=4, widget=forms.TextInput(attrs={'class': 'form-input w-input', 'placeholder': 'CVV'}))
    amount_to_pay = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput(attrs={'class': 'form-input w-input', 'placeholder': 'Amount to Pay'}))

class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['full_name', 'email', 'phone', 'resume']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'w-input', 'placeholder': 'Full Name'}),
            'email': forms.EmailInput(attrs={'class': 'w-input', 'placeholder': 'Email Address'}),
            'phone': forms.TextInput(attrs={'class': 'w-input', 'placeholder': 'Phone Number'}),
            'resume': forms.FileInput(attrs={'class': 'w-input', 'accept': '.pdf,.doc,.docx'}),
        }

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['reviewer_name', 'title', 'rating', 'content', 'reviewer_image']
        widgets = {
            'reviewer_name': forms.TextInput(attrs={'class': 'w-input', 'placeholder': 'Your Name'}),
            'title': forms.TextInput(attrs={'class': 'w-input', 'placeholder': 'Review Title'}),
            'rating': forms.NumberInput(attrs={'class': 'w-input', 'min': 1, 'max': 5, 'placeholder': '5'}),
            'content': forms.Textarea(attrs={'class': 'w-input', 'placeholder': 'Write your review here...', 'rows': 4}),
            'reviewer_image': forms.FileInput(attrs={'class': 'w-input', 'accept': 'image/*'})
        }
