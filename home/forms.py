from django import forms


# Contact Form
class ContactForm(forms.Form):

    name = forms.CharField(max_length=63, required=True, widget=forms.TextInput(attrs={'placeholder': _('Naam en Voornaam')}))
    company = forms.CharField(max_length=28, required=True, widget=forms.TextInput(attrs={'placeholder': _('Bedrijf')}))
    email = forms.EmailField(max_length=63, required=True, widget=forms.TextInput(attrs={'placeholder': _('Email')}))
    message = forms.CharField(required=False, widget=forms.Textarea(attrs={'placeholder': _('Jouw boodschap')}))
