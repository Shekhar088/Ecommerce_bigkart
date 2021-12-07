from django import forms
from django.forms import fields
from .models import RatingReview

class ReviewForm(forms.ModelForm):
    class Meta:
        model = RatingReview
        fields = ['subject', 'review', 'rating']
