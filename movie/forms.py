from django import forms
from .models import Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['text', 'rating', 'watchAgain']
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your review here...'}),
            'rating': forms.RadioSelect(choices=Review.STAR_CHOICES),  # Display as radio buttons
            'watchAgain': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
from django import forms
from .models import MovieRequest

class MovieRequestForm(forms.ModelForm):
    class Meta:
        model = MovieRequest
        fields = ['movie_name', 'language', 'year']
