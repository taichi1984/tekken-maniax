from django import forms




class StreamSearchForm(forms.Form):
    query = forms.CharField(max_length=100,
                            required=False,
                            label="配信者、配信チャンネル検索",
                            widget=forms.TextInput(attrs={'class':'search_text_form'}))
    

class StreamSortForm(forms.Form):
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