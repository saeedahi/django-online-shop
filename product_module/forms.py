from django import forms
from django.core import validators


class CommentForm(forms.Form):
    comment = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'نظر شما درباره این محصول چیست؟',
            'id': 'commentText',
            'name': 'comment'
        }),
        validators=[
            validators.MaxLengthValidator(500),
        ]
    )