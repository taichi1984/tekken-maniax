from django import forms
from .models import Tag



class ChannelSearchForm(forms.Form):
    query = forms.CharField(max_length=100,
                            required=False,
                            label="チャンネルタイトル、タグ検索",
                            widget=forms.TextInput(attrs={'class':'search_text_form'}))
    

class ChannelSortForm(forms.Form):
    channel_sort_field = forms.ChoiceField(
        choices = [
                ('viewcount_desc','閲覧回数が多い順'),
                ('viewcount_asc','閲覧回数が少ない順'),
                ('subscribercount_desc','チャンネル登録者数が多い順'),
                ('subscribercount_asc','チャンネル登録者数が少ない順'),
                ('videocount_desc','投稿動画数が多い順'),
                ('videocount_asc','投稿動画数が少ない順')
                ],

        widget=forms.Select(attrs={'class': 'sort_select_form'}),
        label='並び替え',
        required=False,
   
    )

class VideoSearchForm(forms.Form):
    query = forms.CharField(
        max_length=100,
        required=False)


class TagForm(forms.ModelForm):
    new_tag = forms.CharField(label="新しいタグ" ,max_length=100,required=False)
    
    class Meta:
        model = Tag
        fields = ['new_tag']




