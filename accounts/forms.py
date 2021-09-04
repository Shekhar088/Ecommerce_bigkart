from django import forms
from .models import Account

class RegisterForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter your password again'
    }))
    class Meta:

        model = Account
        fields = ['first_name', 'last_name', 'password', 'email', 'phone_number']

    def __init__(self,*args,**kwargs):
        super(RegisterForm, self).__init__(*args,**kwargs)
        self.fields['first_name'].widget.attrs['placeholder']= 'Your first name'
        self.fields['last_name'].widget.attrs['placeholder']= 'Your last name'
        self.fields['email'].widget.attrs['placeholder']= 'Your Email'
        self.fields['phone_number'].widget.attrs['placeholder']= 'Enter phone number'

        for field in self.fields:
            self.fields[field].widget.attrs['class']= 'form-control'

    def clean(self):
        cleaned_data =super(RegisterForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!!"
            )