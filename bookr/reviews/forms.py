from django import forms
from .models import Publisher, Review


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(
        required=False, choices=(("title", "Title"), ("contributor", "Contributor"))
    )


# ModelForm builds a form from a model
class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        # Include all the fields in the model using fields = "__all__" or exclude = ()
        fields = "__all__"


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ("date_edited", "book")

    # Override rating field
    rating = forms.IntegerField(min_value=0, max_value=5)
