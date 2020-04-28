from django import forms
from guide.models import Character, Category


class CommentSubmitForm(forms.Form):
    comment = forms.CharField(label="コメント", widget=forms.Textarea)


class SearchGuideForm(forms.Form):
    search_word = forms.CharField(max_length=50)


