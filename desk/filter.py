from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateTimeFilter
from .models import Post, User, Comment
from django import forms


class PostFilter(FilterSet):
    date = DateTimeFilter(field_name='created_at', lookup_expr='gt', label='Начиная с даты')
    date.field.widget = forms.DateTimeInput(attrs={'type': 'date'})
    title = CharFilter(field_name='title', lookup_expr='contains', label='Заголовок содержит')
    author = ModelChoiceFilter(
        field_name='author',
        empty_label='Любой',
        queryset=User.objects.all(),
        label='Автор'
    )

    class Meta:
       model = Post
       fields = ['title', 'date', 'author']


class CommentFilter(FilterSet):
    date = DateTimeFilter(field_name='created_at', lookup_expr='gt', label='Начиная с даты')
    date.field.widget = forms.DateTimeInput(attrs={'type': 'date'})
    text = title = CharFilter(field_name='text', lookup_expr='contains', label='Текст сообщения')
    sender = ModelChoiceFilter(
        field_name='sender',
        empty_label='Любой',
        queryset=User.objects.all(),
        label='Отправитель'
    )
    target_user = ModelChoiceFilter(
        field_name='target_user',
        empty_label='Любой',
        queryset=User.objects.all(),
        label='Получатель'
    )

    class Meta:
       model = Comment
       fields = ['text', 'date', 'sender', 'target_user']