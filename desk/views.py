from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import BaseRegisterForm, SignInForm, CheckCodeForm
from django.core.mail import send_mail

from desk.models import Post, OneTimeCode, Comment
from django.contrib.auth.models import User
import time, random


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
        return context

def like(request):
    post = Post.objects.filter(pk=request.pk)
    post.like()
    post.save()

def dislike(request):
    post = Post.objects.filter(pk=request.pk)
    post.dislike()
    post.save()

class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

# class PostUpdate(UpdateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'post_edit.html'
#     success_url = '/'


class PostDelete(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = '/'


class OutCommentList(ListView):
    model = Comment
    ordering = '-created_at'
    template_name = '.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_query_set(self):
        return Comment.objects.filter(author=self.request.user)




def logout_view(request):
    logout(request)
    return redirect('/')

def generate_code():
    t = list(str(time.time()))
    s = random.choices(['q', 'w', 'e', 'r', 't', 'y', 'z', 'x', 'c', 'v'], k=3)
    t.extend(s)
    random.shuffle(t)
    return ''.join(t)

def sign_in_view(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                code = generate_code()
                OneTimeCode.objects.create(user=user, code=code)
                form = CheckCodeForm
                send_mail(
                    "Desk code",
                    f"Ваш код - { code }",
                    'serege1.tashkinov@yandex.ru',
                    [user.email],
                    fail_silently=False,
                )
                render(request, 'sign_in_code.html', {'form': form})
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
            if OneTimeCode.objects.filter(code=code, user__username=user_name).exists():
                user = OneTimeCode.objects.filter(code=code, user__username=user_name).get('user')
                login(request, user)
                return HttpResponseRedirect("/")
            else:
                return HttpResponseRedirect("/signin")
    form = CheckCodeForm
    return render(request, 'sign_in_code.html', {'form': form})


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'

