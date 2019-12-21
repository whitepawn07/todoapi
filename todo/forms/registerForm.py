from django import forms
from todo.models import Profile

class SignupForm(forms.ModelForm):
    """
       Sign up Users
    """
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, required=True, help_text='Required. Inform a valid email address.')

    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta(object):
        model = Profile
        fields = ("email", "first_name", "last_name")
    
    def clean_password2(self):
        #confirm password
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        #save the provided password and encrypt
        user = super(SignupForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
