from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from .models import User


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'address', 'about_user', 'phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'آدرس',
                'rows': 3,
            }),
            'about_user': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'درباره شخص',
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'شماره موبایل'
            })
        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'address': 'آدرس',
            'about_user': 'درباره شخص',
            'phone_number': 'شماره موبایل'
        }


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='نام',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    last_name = forms.CharField(
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label='تکرار رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']

        if confirm_password == password:
            return confirm_password

        raise ValidationError('کلمه عبور و تکرار کلمه عبور مغایرت دارند')


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        label='رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )


class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_new_password = forms.CharField(
        label='تکرار کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_new_password(self):
        password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_new_password']

        if confirm_password == password:
            return confirm_password

        raise ValidationError('رمز عبور و تکرار رمز عبور مغایرت دارند')


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='رمز فعلی',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    new_password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_new_password = forms.CharField(
        label='تکرار کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_new_password(self):
        password = self.cleaned_data['new_password']
        confirm_password = self.cleaned_data['confirm_new_password']

        if confirm_password == password:
            return confirm_password

        raise ValidationError('رمز عبور و تکرار رمز عبور مغایرت دارند')