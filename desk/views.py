
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView


from .filter import PostFilter, CommentFilter
from .forms import BaseRegisterForm, SignInForm, CheckCodeForm, CreateCommentForm, PostForm
from .utils import get_subscribed

from desk.models import Post, OneTimeCode, Comment, Subscription
from django.contrib.auth.models import User



# Create your views here.
class PostsList(ListView):
    model = Post
    ordering = '-created_at'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 3


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['subscribed'] = get_subscribed()
        return context

def like_view(request, pk):
    post = Post.objects.get(pk=pk)
    post.like()
    return redirect(request.META.get('HTTP_REFERER'))

def dislike_view(request, pk):
    post = Post.objects.get(pk=pk)
    post.dislike()
    return redirect(request.META.get('HTTP_REFERER'))

class PostsListSearch(ListView):
    model = Post
    ordering = '-created_at'
    template_name = ('post_filter.html')
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_user'] = self.request.user
        context['subscribed'] = get_subscribed()
        return context


class CommentListSearch(ListView):
    model = Comment
    ordering = '-created_at'
    template_name = 'comment_filter.html'
    context_object_name = 'comments'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        qs_out = qs.filter(sender=self.request.user.pk)
        qs_in = qs.filter(target_user=self.request.user.pk)
        letters = (qs_in  | qs_out ).distinct()
        self.filterset = CommentFilter(self.request.GET, letters)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        context['current_user'] = self.request.user
        context['subscribed'] = get_subscribed()
        return context

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        return context

class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/'

    def form_valid(self, form):
        fields = form.save(commit=False)
        fields.author = self.request.user
        fields.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['subscribed'] = get_subscribed()
        return context


class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['subscribed'] = get_subscribed()
        return context


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.request.user
        context['subscribed'] = get_subscribed()
        return context

def delete_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if pk:
        comment.delete()
        return redirect(request.META.get('HTTP_REFERER'))

def confirm_comment(request, pk):
    comment = Comment.objects.get(pk=pk)
    if pk:
        comment.is_confirmed = True
        comment.save()
        return redirect(request.META.get('HTTP_REFERER'))


def send_message_view(request, pk):
    post = Post.objects.filter(pk=pk).select_related('author')[0]
    author = post.author
    if request.method == 'POST':
        form = CreateCommentForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            text = cd['text']
            Comment.objects.create(sender=request.user, target_user=author, text=text, post=post)
            return redirect('/')
        else:
            return HttpResponseRedirect(f"/send_message/{pk}")
    form = CreateCommentForm
    return render(request, 'comment_create.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/')

def sign_in_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect("/signin_code")
            else:
                return HttpResponseRedirect("/signin")
    form = SignInForm
    return render(request, 'sign_in.html', {'form': form})

def sign_in_with_code_view(request):
    if request.method == 'POST':
        form = CheckCodeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_name = cd['username']
            code = cd['code']
            user = User.objects.filter(username=user_name)[0]
            if OneTimeCode.objects.filter(code=code, user__username=user_name).exists():
                login(request, user)
                OneTimeCode.objects.filter(code=code, user__username=user_name).delete()
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("/signin_code")
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    form = CheckCodeForm

    return render(request, 'sign_in_code.html', {'form': form})


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/signin_code'


def subscribe(request):
    Subscription.objects.create(user=request.user)
    return HttpResponseRedirect("/")


