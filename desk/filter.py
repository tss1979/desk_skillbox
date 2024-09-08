from django_filters import FilterSet, ModelChoiceFilter, CharFilter, DateTimeFilter
from .models import Post, User
from django import forms


class PostFilter(FilterSet):
    date = DateTimeFilter(field_name='created_at', lookup_expr='gt', label='Date From')
    date.field.widget = forms.DateTimeInput(attrs={'type': 'date'})
    title = CharFilter(field_name='title', lookup_expr='contains', label='Title contains')
    author = ModelChoiceFilter(
        field_name='author__user__username',
        empty_label='Any',
        queryset=User.objects.all(),
        label='Автор'
    )

    class Meta:
       model = Post
       fields = ['title', 'date', 'author']