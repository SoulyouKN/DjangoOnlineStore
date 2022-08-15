from django import forms

#define register form
class UserForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    email = forms.EmailField(label='电子邮件')

#define login form
class LoginForm(forms.Form):
    username = forms.CharField(label='用户名',max_length=100)
    password = forms.CharField(label='密码',widget=forms.PasswordInput())

#define address form
class AddressForm(forms.Form):
    address = forms.CharField(label='地址', max_length=100)
    phone = forms.CharField(label='电话', max_length=15)
