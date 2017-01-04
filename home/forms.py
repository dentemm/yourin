from django import forms


# Contact Form
class ContactForm(forms.Form):

    name = forms.CharField(max_length=63, required=True, widget=forms.TextInput(attrs={'placeholder': 'Naam en Voornaam'}))
    company = forms.CharField(max_length=28, required=False, widget=forms.TextInput(attrs={'placeholder': 'Bedrijf'}))
    email = forms.EmailField(max_length=63, required=True, widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': 'Jouw boodschap'}))
