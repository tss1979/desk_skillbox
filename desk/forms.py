from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget


from desk.models import Post, Comment


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=SummernoteWidget())

    def __init__(self, *args, **kwags):
        super().__init__(*args, **kwags)


    class Meta:
           model = Post
           fields = [
               'post_kind',
               'title',
               'content',
           ]
           widgets = {
               'title': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
               'post_kind': forms.Select,
           }

class CreateCommentForm(forms.ModelForm):
    class Meta:
           model = Comment
           fields = [
               'text',
           ]
           widgets = {
               'text': forms.TextInput(attrs={'class': 'form-control form-control-lg'}),
           }


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label = "Email")
    first_name = forms.CharField(label = "Имя")
    last_name = forms.CharField(label = "Фамилия")

    class Meta:
        model = User
        fields = ("username",
                  "first_name",
                  "last_name",
                  "email",
                  "password1",
                  "password2", )

class SignInForm(forms.Form):
    username = forms.CharField(label = "Имя")
    password = forms.CharField(widget=forms.PasswordInput)

class CheckCodeForm(forms.Form):
    username = forms.CharField(label = "Логин")
    code = forms.CharField(label = "Код")




