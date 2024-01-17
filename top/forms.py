from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from guide.models import Character
from .models import ChangeLog
from tekkenSite import settings
from django.utils import timezone


class UserProfileCharacterModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "%s %s" % (obj.first_name_jp, obj.family_name_jp)


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'class': 'form_email'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form_username'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form_password1'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form_password2'}))

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
    nick_name = forms.CharField(label="ニックネーム", max_length="50",widget=forms.TextInput(attrs={'class': 'form_nick_name'}))
    main_character = UserProfileCharacterModelChoiceField(queryset=Character.objects.all(), label="メインキャラクター")
    twitter_account = forms.CharField(label="twitter ID", required=False,widget=forms.TextInput(attrs={'class': 'form_twitter'}))
    youtube_channel_url = forms.CharField(label="Youtubeチャンネル URL", required=False,widget=forms.TextInput(attrs={'class': 'form_youtube'}))
    twitch_url = forms.CharField(label="Twitch URL", required=False,widget=forms.TextInput(attrs={'class': 'form_twitch'}))
    introduction = forms.CharField(label="自己紹介", widget=forms.Textarea(attrs={'class': 'form_introduction'}))


class ChangeEmailForm(forms.Form):
    new_email = forms.EmailField(max_length=255,label="新しいEメールアドレス")

class CreateChangeLogForm(forms.ModelForm):
    class Meta:
        model = ChangeLog
        fields = ['pub_date','log']
    
    def __init__(self,*args,**kwargs):
        super(CreateChangeLogForm,self).__init__(*args,**kwargs)
        self.fields['pub_date'].initial = timezone.now()

class UpdateChangeLogForm(forms.ModelForm):
    class Meta:
        model = ChangeLog
        fields = ['pub_date','log']
