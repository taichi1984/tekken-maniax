from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from guide.models import Character
from tekkenSite import settings


class UserProfileCharacterModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.first_name_jp, obj.family_name_jp)


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class UserProfileUpdateForm(forms.Form):
    nick_name = forms.CharField(label="ニックネーム", max_length="50")
    main_character = UserProfileCharacterModelChoiceField(queryset=Character.objects.all(), label="メインキャラクター")
    introduction = forms.CharField(label="自己紹介", widget=forms.Textarea)
