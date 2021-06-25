from .models import Comment, Post
from django import forms
from tinymce import TinyMCE


class TinyMCEWidget(TinyMCE):
    def user_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=TinyMCEWidget(attrs={
        'required': False,
        'cols': 10,
        'rows': 8,
    })
    )

    class Meta:
        model = Post
        fields = '__all__'


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your comment here',
        'type': 'text',
        'rows': 6,
        'cols': 30,
    }), label=False)

    class Meta:
        model = Comment
        fields = ['content']
