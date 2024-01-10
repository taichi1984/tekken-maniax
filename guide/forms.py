from django import forms
from guide.models import Character, Category,Guide
from ckeditor.widgets import CKEditorWidget

class CommentSubmitForm(forms.Form):
    comment = forms.CharField(label="コメント", widget=forms.Textarea)


class SearchGuideForm(forms.Form):
    search_word = forms.CharField(max_length=50)

class CreateGuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields =[
            "category",
            "character",
            "title",
            "article",
            "number_of_preview",
            "publishing_setting",
            "is_deleted",
        ]
        initial_data={
            'is_deleted':False,
            'number_of_preview':0,
        }
        labels={
            'category':"カテゴリ　　",
            'character':"キャラクター",
            'title':"タイトル　　",
            'publishing_setting':"公開する",
            'article':""
        }
        widgets ={
            'category':forms.Select(attrs={'class': 'guide_form_category'}),
            'character':forms.Select(attrs={'class': 'guide_form_character'}),
            'title':forms.TextInput(attrs={'class': 'guide_form_title'}),
            'author':forms.HiddenInput(),
            'article':CKEditorWidget(),
            'pub_date':forms.HiddenInput(),
            'update_date':forms.HiddenInput(),
            'number_of_preview':forms.HiddenInput(),
            'publishing_setting':forms.CheckboxInput(attrs={'class': 'guide_form_publishing_setting'}),
            'is_deleted':forms.HiddenInput(),
        }


       

        def __init__(self, *args, initial_content=None ,**kwargs):
            super(MyModelForm, self).__init__(*args, **kwargs)

            if initial_content is not None:
                self.fields['article'].initial = initial_content
        
        # 各フィールドにクラスを追加
            self.fields['category'].widget.attrs.update({'class': 'guide_form_category'})
            self.fields['character'].widget.attrs.update({'class': 'guide_form_character'})
 

class UpdateGuideForm(forms.ModelForm):
    class Meta:
        model = Guide
        fields =[
            "category",
            "character",
            "title",
            "article",
            "number_of_preview",
            "publishing_setting",
            "is_deleted",
        ]
        labels={
            'category':"カテゴリ　　",
            'character':"キャラクター",
            'title':"タイトル　　",
            'publishing_setting':"公開する",
            'article':""
        }

        widgets ={
            'category':forms.Select(attrs={'class': 'guide_form_category'}),
            'character':forms.Select(attrs={'class': 'guide_form_character'}),
            'title':forms.TextInput(attrs={'class': 'guide_form_title'}),
            'author':forms.HiddenInput(),
            'article':CKEditorWidget(),
            'pub_date':forms.HiddenInput(),
            'update_date':forms.HiddenInput(),
            'number_of_preview':forms.HiddenInput(),
            'publishing_setting':forms.CheckboxInput(attrs={'class': 'guide_form_publishing_setting'}),
            'is_deleted':forms.HiddenInput(),
        }


        def __init__(self, *args, initial_content=None ,**kwargs):
            
            super(MyModelForm, self).__init__(*args, **kwargs)
             # 各フィールドにクラスを追加
            self.fields['category'].widget.attrs.update({'class': 'guide_form_category'})
            self.fields['character'].widget.attrs.update({'class': 'guide_form_character'})

       
    
    