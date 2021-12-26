from .models import Comment, Post, Contact
from django import forms
from tinymce import TinyMCE
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Field, Submit


class TinyMCEWidget(TinyMCE):
    def user_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={
                "required": False,
                "cols": 10,
                "rows": 8,
            }
        )
    )

    class Meta:
        model = Post
        fields = "__all__"


class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your comment here",
                "type": "text",
                "rows": 6,
                "cols": 30,
            }
        ),
        label=False,
    )

    class Meta:
        model = Comment
        fields = ["content"]


class ContactForm(forms.ModelForm):
    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your Message",
            }
        )
    )
    name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your name",
            }
        )
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            }
        )
    )
    subject = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your subject",
            }
        )
    )

    class Meta:
        model = Contact
        fields = (
            "name",
            "email",
            "subject",
            "message",
        )

    def __init__(self, *args, **kwargs):

        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = "contactForm"
        self.helper.form_class = "bg-light p-5 contact-form"
        self.helper.form_show_labels = False

        self.helper.layout = Layout(
            Div(
                Div(
                    Div(Field("name"), css_class="f-group"),
                    css_class="col-lg-4 col-md-6",
                ),
                Div(
                    Div(Field("email"), css_class="fo-group"),
                    css_class="col-lg-4 col-md-6",
                ),
                Div(
                    Div(Field("subject"), css_class="form-group"),
                    css_class="col-lg-4 col-md-6",
                ),
                Div(
                    Div(Field("message"), css_class="form-group"),
                    Div(
                        Submit(
                            "contact-me",
                            "Send Message",
                            css_class="btn btn-primary btn-block py-3 px-5",
                        ),
                        css_class="form-group",
                    ),
                    css_class="col-lg-12",
                ),
                css_class="row",
            ),
        )
