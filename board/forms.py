from django import forms
from .models import Board

from django_summernote.fields import SummernoteTextField
from django_summernote.widgets import SummernoteWidget


class BoardWriteForm(forms.ModelForm):
    post_title = forms.CharField(
        label='글 제목',
        widget=forms.TextInput(
            attrs={
                'placeholder': '게시글 제목'
            }
        ),
        required=True,
    )
    post_content = SummernoteTextField()

    field_order = [
        'post_title',
        'post_content',
    ]

    class Meta:
        model = Board
        fields = [
            'post_title',
            'post_content',
        ]

        widgets = {
            'post_content':SummernoteWidget(),
        }

    def clean(self):
        cleaned_data = super().clean()

        post_title = cleaned_data.get('post_title', '')
        post_content = cleaned_data.get('post_content', '')

        if post_title == '':
            self.add_error('post_title', '글 제목을 입력하세요.')
        elif post_content == '':
            self.add_error('post_content', '글 내용을 입력하세요.')
        else:
            self.post_title = post_title
            self.post_content = post_content
